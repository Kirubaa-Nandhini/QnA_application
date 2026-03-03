from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from .models import Question, Tag, Answer, Vote, Comment
from .forms import QuestionForm, AnswerForm

from django.db import models
from django.db.models import Count, Q, Sum

class VoteToggleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        content_type_id = request.POST.get('content_type_id')
        object_id = request.POST.get('object_id')
        
        try:
            vote_value = int(request.POST.get('value', 0))
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid vote value'}, status=400)

        if vote_value not in [1, -1]:
            return JsonResponse({'error': 'Invalid vote value'}, status=400)

        content_type = get_object_or_404(ContentType, id=content_type_id)
        obj = get_object_or_404(content_type.model_class(), id=object_id)

        # check if it is the author trying to vote
        if hasattr(obj, 'author') and obj.author == request.user:
            return JsonResponse({'error': 'You cannot vote on your own content'}, status=403)

        vote, created = Vote.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=object_id,
            defaults={'value': vote_value}
        )

        if not created:
            if vote.value == vote_value:
                # toggle off if same value
                vote.delete()
                action = 'removed'
            else:
                # change vote value
                vote.value = vote_value
                vote.save()
                action = 'changed'
        else:
            action = 'added'

        return JsonResponse({
            'score': obj.score,
            'action': action
        })

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        content_type_id = request.POST.get('content_type_id')
        object_id = request.POST.get('object_id')
        content = request.POST.get('content', '').strip()
        parent_id = request.POST.get('parent_id')

        if not content:
            return redirect(request.META.get('HTTP_REFERER', 'question_list'))

        content_type = get_object_or_404(ContentType, id=content_type_id)
        
        parent_comment = None
        if parent_id and str(parent_id).isdigit():
            parent_comment = Comment.objects.filter(id=parent_id).first()

        Comment.objects.create(
            user=request.user,
            content_type=content_type,
            object_id=object_id,
            content=content,
            parent=parent_comment
        )

        return redirect(request.META.get('HTTP_REFERER', 'question_list'))

class QuestionListView(ListView):
    model = Question
    template_name = 'questions/question_list.html'
    context_object_name = 'questions'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().annotate(
            num_answers=Count('answers', distinct=True),
            total_score=Sum('votes__value')
        )
        tag_name = self.request.GET.get('tag')
        sort = self.request.GET.get('sort', 'newest')
        query = self.request.GET.get('q')
        
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()

        if tag_name:
            queryset = queryset.filter(tags__name=tag_name)
        
        if sort == 'oldest':
            queryset = queryset.order_by('created_at')
        else:
            queryset = queryset.order_by('-created_at')
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['current_sort'] = self.request.GET.get('sort', 'newest')
        context['current_tag'] = self.request.GET.get('tag', '')
        context['current_query'] = self.request.GET.get('q', '')
        return context

class QuestionDetailView(DetailView):
    model = Question
    template_name = 'questions/question_detail.html'
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()
        user = self.request.user
        
        context['answer_form'] = AnswerForm()
        context['question_ct'] = ContentType.objects.get_for_model(Question).id
        context['answer_ct'] = ContentType.objects.get_for_model(Answer).id
        
        # Performance: Pre-fetch current user's votes to avoid N+1 problem in template
        user_votes = {}
        if user.is_authenticated:
            # Fetch votes for the question
            q_vote = Vote.objects.filter(user=user, content_type_id=context['question_ct'], object_id=question.id).first()
            if q_vote:
                user_votes[f"q_{question.id}"] = q_vote.value
                
            # Fetch votes for all answers in one query
            answer_ids = question.answers.values_list('id', flat=True)
            a_votes = Vote.objects.filter(user=user, content_type_id=context['answer_ct'], object_id__in=answer_ids)
            for v in a_votes:
                user_votes[f"a_{v.object_id}"] = v.value
                
        context['user_votes'] = user_votes

        # Related Questions: Find questions with at least one shared tag, ranked by similarity
        related_questions = Question.objects.filter(
            tags__in=question.tags.all()
        ).exclude(id=question.id).annotate(
            num_shared_tags=Count('tags')
        ).select_related('author').prefetch_related('tags', 'answers').order_by('-num_shared_tags', '-created_at').distinct()[:5]
        
        context['related_questions'] = related_questions
        return context

class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'questions/question_form.html'
    success_url = reverse_lazy('question_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'questions/question_form.html'
    success_url = reverse_lazy('question_list')

    def test_func(self):
        question = self.get_object()
        return self.request.user == question.author

class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    template_name = 'questions/question_confirm_delete.html'
    success_url = reverse_lazy('question_list')

    def test_func(self):
        question = self.get_object()
        return self.request.user == question.author

class AnswerCreateView(LoginRequiredMixin, CreateView):
    model = Answer
    form_class = AnswerForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.question = get_object_or_404(Question, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('question_detail', kwargs={'pk': self.kwargs['pk']})

class AnswerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'questions/answer_form.html'

    def test_func(self):
        answer = self.get_object()
        return self.request.user == answer.author

    def get_success_url(self):
        return reverse_lazy('question_detail', kwargs={'pk': self.object.question.pk})

class AnswerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Answer
    template_name = 'questions/answer_confirm_delete.html'

    def test_func(self):
        answer = self.get_object()
        return self.request.user == answer.author

    def get_success_url(self):
        return reverse_lazy('question_detail', kwargs={'pk': self.object.question.pk})

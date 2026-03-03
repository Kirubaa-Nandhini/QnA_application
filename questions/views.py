from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Question, Tag, Answer
from .forms import QuestionForm, AnswerForm

from django.db.models import Count

class QuestionListView(ListView):
    model = Question
    template_name = 'questions/question_list.html'
    context_object_name = 'questions'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().annotate(
            num_answers=Count('answers')
        )
        tag_name = self.request.GET.get('tag')
        sort = self.request.GET.get('sort', 'newest')
        
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
        return context

class QuestionDetailView(DetailView):
    model = Question
    template_name = 'questions/question_detail.html'
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answer_form'] = AnswerForm()
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

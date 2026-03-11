from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='votes')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    value = models.SmallIntegerField() # 1 for upvote, -1 for downvote
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.content_object}"

    class Meta:
        ordering = ['created_at']

class Question(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='questions')
    tags = models.ManyToManyField(Tag, related_name='questions')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    votes = GenericRelation(Vote)
    comments = GenericRelation(Comment)

    def __str__(self):
        return self.title

    @property
    def score(self):
        return self.votes.aggregate(total=models.Sum('value'))['total'] or 0

    def get_user_vote(self, user):
        if not user.is_authenticated:
            return 0
        vote = self.votes.filter(user=user).first()
        return vote.value if vote else 0

    class Meta:
        ordering = ['-created_at']

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    votes = GenericRelation(Vote)
    comments = GenericRelation(Comment)

    def __str__(self):
        return f"Answer by {self.author.username} on {self.question.title}"

    @property
    def score(self):
        return self.votes.aggregate(total=models.Sum('value'))['total'] or 0

    def get_user_vote(self, user):
        if not user.is_authenticated:
            return 0
        vote = self.votes.filter(user=user).first()
        return vote.value if vote else 0

    class Meta:
        ordering = ['-created_at']

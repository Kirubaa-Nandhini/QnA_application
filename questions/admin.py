from django.contrib import admin
from .models import Question, Tag, Answer

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('author', 'question', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'author__username', 'question__title')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    list_filter = ('created_at', 'tags')
    search_fields = ('title', 'description', 'author__username')
    filter_horizontal = ('tags',)

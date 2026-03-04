from django.contrib import admin
from .models import Question, Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    list_filter = ('created_at', 'tags')
    search_fields = ('title', 'description', 'author__username')
    filter_horizontal = ('tags',)

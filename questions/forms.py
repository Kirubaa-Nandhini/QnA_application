from django import forms
from .models import Question, Tag, Answer
from django.utils.text import slugify

class QuestionForm(forms.ModelForm):
    tags_input = forms.CharField(
        max_length=255, 
        required=False, 
        label="Tags",
        help_text="Enter tags separated by commas (e.g. python, django, coding)",
        widget=forms.TextInput(attrs={'placeholder': 'e.g. python, django, web'})
    )

    class Meta:
        model = Question
        fields = ['title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Describe your question in detail...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['tags_input'].initial = ", ".join([t.name for t in self.instance.tags.all()])

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if commit:
            instance.save()
            # Handle tags
            tags_str = self.cleaned_data.get('tags_input', '')
            tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
            
            # Clear existing tags
            instance.tags.clear()
            for name in tag_names:
                # Normalize name to lowercase for consistency
                normalized_name = name.lower()
                
                # Check for existing tag or create it atomically
                tag, created = Tag.objects.get_or_create(name=normalized_name)
                    
                instance.tags.add(tag)
                
        return instance

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write your answer here...'}),
        }

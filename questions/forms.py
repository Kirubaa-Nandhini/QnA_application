from django import forms
from .models import Question, Tag
from django.utils.text import slugify

class QuestionForm(forms.ModelForm):
    tags = forms.CharField(
        max_length=255, 
        required=False, 
        help_text="Enter tags separated by commas (e.g. python, django, coding)",
        widget=forms.TextInput(attrs={'placeholder': 'e.g. python, django, web'})
    )

    class Meta:
        model = Question
        fields = ['title', 'description', 'tags']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Describe your question in detail... (Markdown supported)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['tags'].initial = ", ".join([t.name for t in self.instance.tags.all()])

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if commit:
            instance.save()
            # Handle tags
            tags_str = self.cleaned_data.get('tags', '')
            tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
            
            # Clear existing tags
            instance.tags.clear()
            for name in tag_names:
                # Normalize name to lowercase for consistency
                normalized_name = name.lower()
                tag_slug = slugify(normalized_name) or 'tag'
                
                # Check for existing tag by slug or name
                tag = Tag.objects.filter(slug=tag_slug).first()
                if not tag:
                    tag = Tag.objects.filter(name=normalized_name).first()
                
                if not tag:
                    # Create new tag; the model's save() will handle uniqueness
                    tag = Tag.objects.create(name=normalized_name)
                    
                instance.tags.add(tag)
                
        return instance

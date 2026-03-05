try:
    import markdown2
    USE_MARKDOWN2 = True
except ImportError:
    import markdown
    USE_MARKDOWN2 = False

import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='markdownify')
def markdownify(text):
    if not text:
        return ""
    
    # Pre-processing: Ensure a blank line before lists if they follow text
    # This addresses the strictness of many Markdown parsers where lists 
    # must be preceded by a blank line to be recognized as blocks.
    # regex matches: (not a newline) + newline + (list marker)
    text = re.sub(r'([^\n])\n(\s*[\*\-\+] )', r'\1\n\n\2', text)
    text = re.sub(r'([^\n])\n(\s*\d+\. )', r'\1\n\n\2', text)

    try:
        if USE_MARKDOWN2:
            html = markdown2.markdown(text, extras=[
                'fenced-code-blocks', 
                'tables', 
                'sane-lists',
                'header-ids',
                'task_lists',
                'strike',
                'code-friendly'
            ])
            return mark_safe(html)
        else:
            # Removed 'nl2br' as it can sometimes conflict with list detection
            # by turning functional newlines into literal <br> tags within a paragraph
            html = markdown.markdown(text, extensions=['extra', 'codehilite', 'sane_lists', 'smarty'])
            return mark_safe(html)
    except Exception as e:
        # Final fallback
        if USE_MARKDOWN2:
            return mark_safe(markdown2.markdown(text))
        else:
            return mark_safe(markdown.markdown(text))

import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='markdownify')
def markdownify(text):
    if not text:
        return ""
    try:
        # 'extra' includes fused_code, tables, footnotes, etc.
        html = markdown.markdown(text, extensions=['extra', 'codehilite'])
        return mark_safe(html)
    except Exception as e:
        # Fallback to basic if extensions fail
        return mark_safe(markdown.markdown(text))

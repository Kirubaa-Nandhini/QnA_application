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

    # Ensure blank line before lists for proper markdown parsing
    text = re.sub(r'([^\n])\n(\s*[\*\-\+] )', r'\1\n\n\2', text)
    text = re.sub(r'([^\n])\n(\s*\d+\. )', r'\1\n\n\2', text)

    try:
        if USE_MARKDOWN2:
            html = markdown2.markdown(
                text,
                extras=[
                    "fenced-code-blocks",
                    "tables",
                    "sane-lists",
                    "header-ids",
                    "task_lists",
                    "strike",
                    "code-friendly",
                ],
            )
        else:
            html = markdown.markdown(
                text,
                extensions=["extra", "codehilite", "sane_lists", "smarty"],
            )

        return mark_safe(html)

    except Exception:
        # Final fallback if advanced markdown parsing fails
        if USE_MARKDOWN2:
            return mark_safe(markdown2.markdown(text))
        else:
            return mark_safe(markdown.markdown(text))


@register.filter(name='get_user_vote')
def get_user_vote(obj, user):
    if hasattr(obj, "get_user_vote"):
        return obj.get_user_vote(user)
    return 0
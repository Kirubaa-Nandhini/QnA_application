from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    """
    Returns the URL-encoded querystring for the current page,
    updating the params with the key/value pairs passed to the tag.
    Keys with empty string values will be removed.
    """
    request = context.get('request')
    if request:
        updated = request.GET.copy()
        for k, v in kwargs.items():
            if v is not None and str(v) != '':
                updated[k] = v
            else:
                updated.pop(k, 0)
        return f"?{updated.urlencode()}"
    return ""

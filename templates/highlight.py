from django import template
from django.utils.html import mark_safe
from re import IGNORECASE, compile, escape as rescape

register = template.Library()

@register.filter(name='highlight')
def highlight(text, search):
    # создаем регулярное выражение с параметром q, игнорируя регистр
    rgx = compile(rescape(search), IGNORECASE)
    return mark_safe(rgx.sub(lambda m: f'<mark>{m.group()}</mark>', text))
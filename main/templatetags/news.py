from django import template

register = template.Library()


@register.filter
def latest_three_news(value):
    return value[:3]

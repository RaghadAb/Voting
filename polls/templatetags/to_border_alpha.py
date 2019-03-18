from django import template

register = template.Library()

@register.filter(name="to_border_alpha")
def to_border_alpha(value):
    return value.replace("1.0","0.3")

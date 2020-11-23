from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    return value * arg

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def has_item(dictionary, key):
    return key in dictionary

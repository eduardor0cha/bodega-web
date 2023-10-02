from django import template

register = template.Library()


@register.filter
def calcDiscount(value, arg):
    return value - (value * arg)


@register.filter
def multiply(value, arg):
    return value * arg


@register.filter
def index(indexable, i):
    return indexable[i]

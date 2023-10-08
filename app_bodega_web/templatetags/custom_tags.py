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


@register.filter
def formatToCurrency(value):
    newValue = f"{value:.2f}".replace(".", ",")
    index = newValue.find(",")
    for i in range(index - 3, 0, -3):
        newValue = newValue[:i] + "." + newValue[i:]

    return newValue


@register.filter
def formatPercentage(value):
    formattedValue = f"{float(value) * 100:.1f}"

    if (float(formattedValue) == int(float(formattedValue))):
        return int(float(formattedValue))
    else:
        return formattedValue

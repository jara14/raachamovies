from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    """
    Add a CSS class to an HTML element or form field widget.

    Usage:
        {{ form.field_name|add_class:"class-name" }}
    """
    if hasattr(value, 'as_widget'):  # Checking if the value is a form field widget
        return value.as_widget(attrs={'class': arg})
    return value + ' ' + arg


@register.filter
def multiply(value, arg):
    return value * arg
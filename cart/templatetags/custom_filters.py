from django import template

register=template.Library()


@register.filter(name='mul')
# function for multiplication 
def multiplication(v1,v2):
    return v1*v2
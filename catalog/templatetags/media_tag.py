from django import template

register = template.Library()


@register.simple_tag
def media_tag(product):
    return product.image.url

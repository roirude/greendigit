from django import template

from slippers.templatetags.slippers import register_components

register = template.Library()

register_components(
    {
        "product_card": "products/components/product_card.html",
    },
    register,
)

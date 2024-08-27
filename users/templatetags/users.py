from django import template

from slippers.templatetags.slippers import register_components

register = template.Library()

register_components(
    {
        "farmer": "components/farmer.html",
    },
    register,
)

from django import template

from slippers.templatetags.slippers import register_components

register = template.Library()

register_components(
    {
        "farmer": "components/farmer.html",
    },
    register,
)


@register.filter
def mask_email(email):
    try:
        user, domain = email.split('@')
        masked_user = user[0] + '*' * (len(user) - 2) #+ user[-1]
        return masked_user + '@' + domain
    except ValueError:
        return email  
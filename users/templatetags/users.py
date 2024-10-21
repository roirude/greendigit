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
        masked_user = '*' * (len(user) - 2) #+ user[-1]
        return masked_user + '@' + '*****'
    except ValueError:
        return email
    

@register.filter
def mask_tel(phone_number):
    try:
        masked_phone_number = '*' * (len(phone_number) - 2) + phone_number[-2] + phone_number[-1]
        return masked_phone_number
    except ValueError:
        return phone_number
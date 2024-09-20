from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver

from comparison.models import ProductComparison


@receiver(user_logged_out)
def clear_product_comparison_on_logout(sender, request, user, **kwargs):
    ProductComparison.objects.filter(user=user).delete()
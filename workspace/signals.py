from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .utils import log_action


@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    log_action(user, "login")


@receiver(user_logged_out)
def on_user_logged_out(sender, request, user, **kwargs):
    log_action(user, "logout")

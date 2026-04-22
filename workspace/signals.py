from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)
from django.dispatch import receiver
from .utils import log_action


def get_ip(request):
    """
    Récupère l'adresse IP réelle de l'utilisateur.
    Tient compte des procys et reverse proxys (ex: Nginx).
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    ip = get_ip(request)
    log_action(user, "login", ip_adress=ip)


@receiver(user_logged_out)
def on_user_logged_out(sender, request, user, **kwargs):
    ip = get_ip(request)
    log_action(user, "logout", ip_adress=ip)


@receiver(user_login_failed)
def on_user_login_failed(sender, credentials, request, **kwargs):
    ip = get_ip(request)
    username = credentials.get("username", "inconnu")
    log_action(
        None,
        "login_failed",
        detail=f"Tentative avec l'identifiant : {username}",
        ip_adress=ip,
    )

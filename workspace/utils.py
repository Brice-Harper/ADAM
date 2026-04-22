from .models import Log


def log_action(user, action, detail="", ip_adress=None):
    """Enregistre une action  dans les logs

    Utilisation :
        log_action(request.user, "note_create", "Titre de la note")
        log_action(request.user, "login", ip_adress="192.168.1.1")
    """
    Log.objects.create(
        user=user,
        action=action,
        detail=detail,
        ip_adress=ip_adress,
    )

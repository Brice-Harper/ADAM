from .models import Log


def log_action(user, action, detail=""):
    """Enregistre une action  dans les logs

    Utilisation :
        log_action(request.user, "note_create", "Titre de la note")
    """
    Log.objects.create(user=user, action=action, detail=detail)

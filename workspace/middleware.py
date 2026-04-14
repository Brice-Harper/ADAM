from django.shortcuts import redirect
from django.urls import reverse


class WorkspaceLoginRequiredMiddleware:
    """
    Middleware to ensure that users are authenticated before accessing workspace-related views.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Chemin demandé par le navigateur (ex : /app/, /admin/, etc.)
        path = request.path

        # Si on est dans /app/ et que l'utilisateur n'est pas connecté
        if path.startswith("/app/") and not request.user.is_authenticated:
            return redirect(reverse("login"))  # Redirige vers la page de connexion

        # Sinon, on laisse Django continuer normalement
        response = self.get_response(request)
        return response

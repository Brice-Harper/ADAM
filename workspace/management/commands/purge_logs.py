from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from workspace.models import Log
from workspace.utils import log_action


class Command(BaseCommand):
    help = "Supprime les logs de plus de 6 mois"

    def handle(self, *args, **options):
        limite = timezone.now() - timedelta(days=180)
        anciens_logs = Log.objects.filter(created_at__lt=limite)
        nombre = anciens_logs.count()
        anciens_logs.delete()

        log_action(
            user=None,
            action="system",
            detail=f"Purge automatique : {nombre} log(s) supprimé(s) (logs de plus de 6 mois)",
        )

        self.stdout.write(
            self.style.SUCCESS(f"{nombre} log(s) supprimé(s) avec succès.")
        )

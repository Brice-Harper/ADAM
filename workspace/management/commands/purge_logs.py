from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from workspace.models import Log


class Command(BaseCommand):
    help = "Supprime les logs de plus de 6 mois"

    def handle(self, *args, **options):
        limite = timezone.now() - timedelta(days=180)
        anciens_logs = Log.objects.filter(created_at__lt=limite)
        nombre = anciens_logs.count()
        anciens_logs.delete()
        self.stdout.write(
            self.style.SUCCESS(f"{nombre} log(s) supprimé(s) avec succès.")
        )

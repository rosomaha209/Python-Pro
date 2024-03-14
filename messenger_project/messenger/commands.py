import os

from django.conf import settings
from django.core.management.base import BaseCommand

from .models import UploadedFile


class Command(BaseCommand):
    help = 'Видаляє записи файлів, які фізично відсутні'

    def handle(self, *args, **options):
        files = UploadedFile.objects.all()
        missing_files = [file for file in files if
                         not os.path.exists(os.path.join(settings.MEDIA_ROOT, file.file.name))]

        if missing_files:
            for missing_file in missing_files:
                self.stdout.write(self.style.WARNING(f'Відсутній файл: {missing_file.file.name}'))
                missing_file.delete()  # Видалення запису з бази даних

            self.stdout.write(self.style.SUCCESS(f'Видалено {len(missing_files)} записів про відсутні файли.'))
        else:
            self.stdout.write(self.style.SUCCESS('Відсутні файли не знайдені.'))

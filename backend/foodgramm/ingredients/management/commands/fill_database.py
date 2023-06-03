import csv
import os
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from ingredients.models import Ingredient


class Command(BaseCommand):
    """Команда для загрузки csv файлов в базу данных:
    python manage.py fill_database"""

    help = "Загрузка информации из csv файлов в базу данных"

    def fill_user(self):
        data_path = os.path.join(
            Path(settings.BASE_DIR).resolve().parent.parent,
            "data\\ingredients.csv"
        )

        with open(data_path, "r", encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1]
                    )

    def handle(self, *args, **options):
        self.fill_user()

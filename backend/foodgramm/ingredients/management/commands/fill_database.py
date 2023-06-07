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

    def fill_ingredients(self):
        self.stdout.write(f"Путь: {settings.BASE_DIR}")
        data_path = os.path.join(
            Path(settings.BASE_DIR),
            "data/ingredients.csv"
        )
       
        with open(data_path, "r", encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1]
                    )

    def handle(self, *args, **kwargs):
        self.stdout.write("Подождите. Заполнение базы данных.")
        self.fill_ingredients()
        self.stdout.write("База данных заполнена")
        

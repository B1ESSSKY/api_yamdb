import os
import csv
from django.core.management.base import BaseCommand
from reviews.models import User, Title, Genre, Category, Comment, Review

CSV_DIR_PATH = "static/data/"

FOREIGN_KEY_FIELDS = ("author", "category")

MODEL_CSV = {
    User: "users.csv",
    Genre: "genre.csv",
    Category: "category.csv",
    Title: "titles.csv",
    Review: "review.csv",
    Comment: "comments.csv",
}


class Command(BaseCommand):
    help = "Загрузка данных из CSV"

    def handle(self, *args, **kwargs):
        for model in MODEL_CSV:
            csv_file_path = os.path.join(CSV_DIR_PATH, MODEL_CSV[model])
            try:
                with open(
                    csv_file_path, newline="", encoding="utf-8"
                ) as csv_file:
                    csv_data = csv.DictReader(csv_file)
                    objs = []
                    for row_number, row in enumerate(csv_data, start=1):
                        for field in FOREIGN_KEY_FIELDS:
                            if field in row:
                                row[f"{field}_id"] = row[field]
                                del row[field]
                        objs.append(model(**row))
                    model.objects.bulk_create(objs, ignore_conflicts=True)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Данные модели {model.__name__} успешно загружены"
                        )
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Ошибка загрузки данных для {csv_file_path}: {e}"
                    )
                )

        load_title_genre(self)


def load_title_genre(self):
    try:
        csv_file_path = os.path.join(CSV_DIR_PATH, "genre_title.csv")

        with open(csv_file_path, newline="", encoding="utf-8") as csv_file:
            csv_data = csv.DictReader(csv_file)
            for row_number, row in enumerate(csv_data, start=1):
                title = Title.objects.get(id=row["title_id"])
                genre = Genre.objects.get(id=row["genre_id"])
                title.genre.add(genre)

            self.stdout.write(
                self.style.SUCCESS(
                    "Данные моделей Title и Genre успешно связаны"
                )
            )
    except Exception as e:
        self.stdout.write(
            self.style.ERROR(f"Ошибка связывания Title и Genre: {e}")
        )

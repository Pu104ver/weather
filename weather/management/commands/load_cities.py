import csv
from django.core.management.base import BaseCommand
from weather.models import City


class Command(BaseCommand):
    help = "Load cities from GeoNames TSV file"

    def add_arguments(self, parser):
        parser.add_argument("filepath", type=str)

    def handle(self, *args, **options):
        filepath = options["filepath"]

        with open(filepath, encoding="utf-8") as file:
            reader = csv.reader(file, delimiter="\t")
            cities = []

            for row in reader:
                try:
                    cities.append(
                        City(
                            geonameid=int(row[0]),
                            name=row[1],
                            asciiname=row[2],
                            alternatenames=row[3],
                            latitude=float(row[4]),
                            longitude=float(row[5]),
                            country_code=row[8],
                            admin1_code=row[10],
                            population=int(row[14]) if row[14].isdigit() else 0,
                            timezone=row[17],
                        )
                    )
                except Exception as e:
                    continue

        City.objects.bulk_create(cities, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f"Загружено {len(cities)} городов."))

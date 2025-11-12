import pandas as pd
from django.core.management.base import BaseCommand
from dashboard.models import BostonQualifier

def to_bool(val):
    if pd.isna(val):
        return False
    val = str(val).strip().lower()
    return val in ('true', '1', 't', 'yes')

def to_int(val):
    if pd.isna(val):
        return None
    return int(val)

def to_float(val):
    if pd.isna(val):
        return None
    return float(val)

class Command(BaseCommand):
    help = "Import BostonQualifier CSV safely using pandas"

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        self.stdout.write(f"Loading CSV from {csv_file}...")

        df = pd.read_csv(csv_file, low_memory=False)

        objects = []
        for _, row in df.iterrows():
            obj = BostonQualifier(
                resultId=row.get('resultId'),
                athleteId=row.get('athleteId'),
                Year=to_int(row.get('Year')),
                Race=row.get('Race'),
                Name=row.get('Name'),
                Country=row.get('Country'),
                Zip=row.get('Zip'),
                City=row.get('City'),
                State=row.get('State'),
                Gender=to_int(row.get('Gender')),
                Age=to_int(row.get('Age')),
                Age_Group=row.get('Age_Group'),
                Finish=to_int(row.get('Finish')),
                OverallPlace=to_int(row.get('OverallPlace')),
                GenderPlace=to_int(row.get('GenderPlace')),
                BQ_2013=to_int(row.get('BQ_2013')),
                BQ_2020=to_int(row.get('BQ_2020')),
                BQ_2026=to_int(row.get('BQ_2026')),
                TotalParticipants=to_int(row.get('TotalParticipants')),
                Date=row.get('Date'),
                RaceCity=row.get('RaceCity'),
                RaceState=row.get('RaceState'),
                RaceCountry=row.get('RaceCountry'),
                BQ=to_bool(row.get('BQ')),
                Qualified=to_bool(row.get('Qualified')),
                Buffer=to_float(row.get('Buffer')),
                Count=to_int(row.get('Count')),
                Run_2025=to_bool(row.get('Run_2025')),
                Distance_to_Boston_mi=to_float(row.get('Distance_to_Boston_mi')),
                Race_Distance_to_Boston_mi=to_float(row.get('Race_Distance_to_Boston_mi')),
                Ran_Boston_2024=to_bool(row.get('Ran_Boston_2024')),
                Avg_Buffer=to_float(row.get('Avg_Buffer')),
                buffer_0_500=to_bool(row.get('buffer_0_500')),
                buffer_500_1000=to_bool(row.get('buffer_500_1000')),
                buffer_1000_1500=to_bool(row.get('buffer_1000_1500')),
                buffer_1500_2000=to_bool(row.get('buffer_1500_2000')),
                buffer_2000_plus=to_bool(row.get('buffer_2000_plus')),
            )
            objects.append(obj)

        self.stdout.write(f"Creating {len(objects)} objects in DB...")
        BostonQualifier.objects.bulk_create(objects, ignore_conflicts=True)
        self.stdout.write("Import finished!")

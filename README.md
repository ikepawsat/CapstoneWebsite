# General Info
1. Start venv
2. Download requirements.txt
3. python manage.py runserver
4. python manage.py migrate (might have to makemigrations first)


Superuser information (for /admin)
-name: BC_Pred
-email: student@bc.edu (irrelevant)
-pass: TheChiefsAreTheBest!


# How to import a csv:
python manage.py import_boston_csv /path/to/your/file.csv
for me: /Users/ike/Downloads/dataset_with_bins.csv so I would run:
python manage.py import_boston_csv /Users/ike/Downloads/dataset_with_bins.csv

# To remove current data:
python manage.py shell
from dashboard.models import BostonQualifier
BostonQualifier.objects.all().delete()
quit()

# To run the model:
python manage.py run_model

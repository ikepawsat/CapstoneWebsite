import os
import numpy as np
from django.core.management.base import BaseCommand
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from dashboard.models import BostonQualifier
import joblib

MODEL_PATH = "dashboard/models/model.pkl"
SCALER_PATH = "dashboard/models/scaler.pkl"

class Command(BaseCommand):
    help = "Train logistic regression model and save it to disk"

    def handle(self, *args, **kwargs):
        qs = BostonQualifier.objects.filter(Buffer__isnull=False)
        X, y = [], []

        for q in qs:
            if None in [q.Country, q.Year, q.Age, q.Gender, q.Race_Distance_to_Boston_mi,
                        q.Count, q.buffer_0_500, q.buffer_500_1000, q.buffer_1000_1500, q.buffer_1500_2000]:
                continue

            X.append([
                float(q.Year),
                float(q.Age),
                float(q.Gender),
                float(q.Ran_Boston_2024),
                float(q.Race_Distance_to_Boston_mi),
                float(q.Count),
                float(q.buffer_0_500),
                float(q.buffer_500_1000),
                float(q.buffer_1000_1500),
                float(q.buffer_1500_2000),
                1.0 if q.Country == "USA" else 0.0,
            ])
            y.append(float(q.Run_2025))

        if len(X) == 0:
            self.stdout.write(self.style.ERROR("No valid data to train model."))
            return

        X = np.array(X, dtype=float)
        y = np.array(y, dtype=float)

        # Standardize
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Train logistic regression
        clf = LogisticRegression(class_weight='balanced', max_iter=1000, solver='lbfgs')
        clf.fit(X_scaled, y)

        # Save model and scaler
        joblib.dump(clf, MODEL_PATH)
        joblib.dump(scaler, SCALER_PATH)

        self.stdout.write(self.style.SUCCESS(f"Model and scaler saved to {MODEL_PATH} and {SCALER_PATH}"))

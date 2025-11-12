import numpy as np
import joblib
from django.core.cache import cache
from dashboard.models import BostonQualifier

CACHE_TIMEOUT = 60 * 60 * 6  # 6 hours
MODEL_PATH = "dashboard/models/model.pkl"
SCALER_PATH = "dashboard/models/scaler.pkl"

def format_time(seconds):
    sign = "-" if seconds < 0 else ""
    seconds = abs(seconds)
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{sign}{minutes}:{secs:02d}"

def predict_cutoff_for_year(n_bootstrap=200, threshold=0.53, size_up_ratio=1, bibs=17800):
    cache_key = "cutoff_prediction_dynamic"
    cached = cache.get(cache_key)
    if cached:
        return cached

    # Load model and scaler
    try:
        clf = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
    except FileNotFoundError:
        return {"error": "Model not trained yet. Run `python manage.py run_model` first."}

    # Build feature array from database
    qs = BostonQualifier.objects.filter(Buffer__isnull=False)
    X = []
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

    if not X:
        return {"error": "No valid data available."}

    X_scaled = scaler.transform(np.array(X, dtype=float))

    y_pred_prob = clf.predict_proba(X_scaled)[:, 1]
    y_pred_class = (y_pred_prob >= threshold).astype(int)
    applicants = int(np.sum(y_pred_class)) * size_up_ratio

    # Bootstrap confidence intervals
    boot_buffers = []
    n = X_scaled.shape[0]
    for _ in range(n_bootstrap):
        idx = np.random.choice(n, n, replace=True)
        Xb = X_scaled[idx]
        ypb = clf.predict_proba(Xb)[:, 1]
        applicants_b = int(np.sum(ypb >= threshold)) * size_up_ratio
        boot_buffers.append((applicants_b - bibs) / 30)

    ci_low, ci_high = np.percentile(boot_buffers, [2.5, 97.5])
    buffer_seconds = (applicants - bibs) / 30
    buffer_time = format_time(buffer_seconds)
    ci_low_time = format_time(ci_low)
    ci_high_time = format_time(ci_high)

    result = {
        "buffer_seconds": buffer_seconds,
        "buffer_time": buffer_time,
        "count": n,
        "applicants": int(applicants) + 24000 - bibs,
        "ci_low": ci_low_time,
        "ci_high": ci_high_time,
    }

    cache.set(cache_key, result, CACHE_TIMEOUT)
    return result

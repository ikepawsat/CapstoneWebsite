from django.shortcuts import render

def home(request):
    return render(request, "home.html")

def explore(request):
    return render(request, "explore.html")

def input_form(request):
    return render(request, "form.html")

def history(request):
    return render(request, "history.html")

# --- Helper 1: Boston Qualifying Time ---
def get_boston_qual_time(age: int, gender: str) -> int:
    """Return Boston Marathon qualifying time (in seconds) for given age and gender."""
    standards = [
        (34, {"M": "2:55:00", "F": "3:25:00"}),
        (39, {"M": "3:00:00", "F": "3:30:00"}),
        (44, {"M": "3:05:00", "F": "3:35:00"}),
        (49, {"M": "3:15:00", "F": "3:45:00"}),
        (54, {"M": "3:20:00", "F": "3:50:00"}),
        (59, {"M": "3:30:00", "F": "4:00:00"}),
        (64, {"M": "3:50:00", "F": "4:20:00"}),
        (69, {"M": "4:05:00", "F": "4:35:00"}),
        (74, {"M": "4:20:00", "F": "4:50:00"}),
        (79, {"M": "4:35:00", "F": "5:05:00"}),
        (200, {"M": "4:50:00", "F": "5:20:00"}),  # 80+
    ]

    gender = gender.upper()[0] if gender else "M"
    if gender not in ("M", "F"):
        raise ValueError("Gender must be 'M' or 'F'")

    for upper_age, times in standards:
        if age <= upper_age:
            h, m, s = map(int, times[gender].split(":"))
            return h * 3600 + m * 60 + s

    # fallback
    return 999999


# --- Helper 2: Convert Seconds to HH:MM:SS ---
def seconds_to_hhmmss(seconds: int, signed: bool = False) -> str:
    """
    Convert seconds to HH:MM:SS format.

    Args:
        seconds (int): Number of seconds.
        signed (bool): If True, prepend '+' for positive or '-' for negative.

    Returns:
        str: Formatted time string.
    """
    abs_seconds = abs(seconds)
    hours = abs_seconds // 3600
    minutes = (abs_seconds % 3600) // 60
    secs = abs_seconds % 60
    time_str = f"{hours:02d}:{minutes:02d}:{secs:02d}"

    if signed:
        return f"Above cutoff by {time_str}" if seconds >= 0 else f"Below cutoff by {time_str}"
    return time_str


# --- Method 3: Django Results View ---
from django.shortcuts import render

def results(request):
    if request.method == "POST":
        time_input = request.POST.get("time")
        age = int(request.POST.get("age"))
        gender = request.POST.get("gender")

        cutoff = int((int(request.POST.get("qualifiers")) -24000) / 30)

        try:
            parts = time_input.split(":")
            # Handle "HH:MM" or "HH:MM:SS"
            if len(parts) == 2:
                h, m = map(int, parts)
                s = 0
            else:
                h, m, s = map(int, parts)
            time_seconds = h * 3600 + m * 60 + s
        except Exception:
            time_seconds = 0

        qual_seconds = get_boston_qual_time(age, gender)
        qualified = time_seconds <= qual_seconds - cutoff
        result = "Qualified" if qualified else "Not Qualified"
        buffer_seconds = int(time_seconds - qual_seconds + cutoff)

        adjusted_qual = int(qual_seconds-cutoff)

        # Use helper to format times
        time_str = seconds_to_hhmmss(time_seconds)
        qual_time_str = seconds_to_hhmmss(qual_seconds)
        buffer_str = seconds_to_hhmmss(buffer_seconds, signed=True)
        predicted_cutoff_time = seconds_to_hhmmss(adjusted_qual)
        cutoff_str = seconds_to_hhmmss(int(cutoff))

        return render(request, "results.html", {
            "time": time_str,
            "age": age,
            "gender": gender,
            "predicted_cutoff": cutoff_str,
            "predicted_cutoff_time": predicted_cutoff_time,
            "qual_time": qual_time_str,
            "result": result,
            "buffer": buffer_str,
        })

    return render(request, "form.html")

from django.db import models

class BostonQualifier(models.Model):
    resultId = models.CharField(max_length=50, primary_key=True)
    athleteId = models.CharField(max_length=50, null=True, blank=True)

    Year = models.IntegerField()
    Race = models.CharField(max_length=200, null=True, blank=True)
    Name = models.CharField(max_length=200, null=True, blank=True)
    Country = models.CharField(max_length=50, null=True, blank=True)
    Zip = models.CharField(max_length=20, null=True, blank=True)
    City = models.CharField(max_length=100, null=True, blank=True)
    State = models.CharField(max_length=20, null=True, blank=True)

    Gender = models.IntegerField()
    Age = models.IntegerField(null=True, blank=True)
    Age_Group = models.CharField(max_length=20, null=True, blank=True)

    Finish = models.IntegerField(null=True, blank=True)
    OverallPlace = models.IntegerField(null=True, blank=True)
    GenderPlace = models.IntegerField(null=True, blank=True)

    BQ_2013 = models.IntegerField(null=True, blank=True)
    BQ_2020 = models.IntegerField(null=True, blank=True)
    BQ_2026 = models.IntegerField(null=True, blank=True)

    TotalParticipants = models.IntegerField(null=True, blank=True)
    Date = models.CharField(max_length=30, null=True, blank=True)

    RaceCity = models.CharField(max_length=100, null=True, blank=True)
    RaceState = models.CharField(max_length=20, null=True, blank=True)
    RaceCountry = models.CharField(max_length=50, null=True, blank=True)

    BQ = models.BooleanField(default=False)
    Qualified = models.BooleanField(default=False)
    Buffer = models.FloatField(null=True, blank=True)

    Count = models.IntegerField(null=True, blank=True)
    Run_2025 = models.BooleanField(default=False)

    Distance_to_Boston_mi = models.FloatField(null=True, blank=True)
    Race_Distance_to_Boston_mi = models.FloatField(null=True, blank=True)

    Ran_Boston_2024 = models.BooleanField(default=False)
    Avg_Buffer = models.FloatField(null=True, blank=True)

    buffer_0_500 = models.BooleanField(default=False)
    buffer_500_1000 = models.BooleanField(default=False)
    buffer_1000_1500 = models.BooleanField(default=False)
    buffer_1500_2000 = models.BooleanField(default=False)
    buffer_2000_plus = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.Name} ({self.Year})"

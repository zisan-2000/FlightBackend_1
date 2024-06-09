from django.db import models

class Plan(models.Model):
    # items = models.CharField(max_length=1000)
    origin = models.CharField(max_length=255, default='DefaultCityValue')
    # region = models.TextField(max_length=255, default='DefaultCityValue')
    # New field for birth_date
    checkinDate = models.DateField(null=True, blank=True)
    checkoutDate = models.DateField(null=True, blank=True)
    def __str__(self):
        return f"Plan {self.id}"


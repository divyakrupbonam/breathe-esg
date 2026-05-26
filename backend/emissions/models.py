from django.db import models
from companies.models import Company
from ingestion.models import DataSource

class EmissionRecord(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'PENDING'),
        ('APPROVED', 'APPROVED'),
        ('REJECTED', 'REJECTED'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    source = models.ForeignKey(
        DataSource,
        on_delete=models.CASCADE
    )

    scope = models.CharField(max_length=20)

    category = models.CharField(max_length=100)

    activity_date = models.DateField()

    activity_value = models.FloatField()

    activity_unit = models.CharField(max_length=50)

    normalized_value = models.FloatField()

    normalized_unit = models.CharField(max_length=50)

    emission_factor = models.FloatField()

    co2e_emission = models.FloatField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    is_flagged = models.BooleanField(default=False)

    flag_reason = models.TextField(
        blank=True,
        null=True
    )

    raw_data = models.JSONField()

    reviewed_at = models.DateTimeField(
        blank=True,
        null=True
    )

    locked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.co2e_emission}"
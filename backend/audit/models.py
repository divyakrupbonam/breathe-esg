from django.db import models
from emissions.models import EmissionRecord

class AuditLog(models.Model):

    record = models.ForeignKey(
        EmissionRecord,
        on_delete=models.CASCADE
    )

    action = models.CharField(max_length=100)

    old_value = models.JSONField(
        null=True,
        blank=True
    )

    new_value = models.JSONField(
        null=True,
        blank=True
    )

    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.action

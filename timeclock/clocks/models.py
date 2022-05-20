from django.db import models
from django.conf import settings
from django.utils.timezone import now


# Create your models here.
class Clock(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    clocked_in = models.DateTimeField(default=now)
    clocked_out = models.DateTimeField(null=True)

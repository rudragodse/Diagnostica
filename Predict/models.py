from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class DiagnosisModel(models.Model):
    patient_name = models.CharField(max_length=100)
    symtoms_entered = models.CharField(max_length=500)
    diagnosis = models.CharField(max_length=120)
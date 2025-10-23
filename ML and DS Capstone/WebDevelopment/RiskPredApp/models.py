from django.db import models

# Create your models here.
class riskPredModel(models.Model):
    Stock = models.CharField(max_length=25, verbose_name="Stock Name", default="Stock")

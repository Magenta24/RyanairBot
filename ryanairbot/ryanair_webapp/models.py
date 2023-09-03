from django.db import models

# Create your models here.

class Airport(models.Model):
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    code = models.CharField(max_length=4)
    currency = models.CharField(max_length=3)

class Flight(models.Model):
    origin_airport = models.ForeignKey(Airport, related_name="origin_city", on_delete=models.PROTECT)
    destination_airport = models.ForeignKey(Airport, related_name="dest_city", on_delete=models.PROTECT)
    date = models.DateField()
    price = models.IntegerField()
    currency = models.CharField(max_length=3)
    search_date = models.DateTimeField()
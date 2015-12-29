from django.db import models


class Bike(models.Model):
    Model = models.CharField(max_length=70)
    Price = models.DecimalField(default=1501.00, max_digits=6, decimal_places=2)
    Best_Use = models.CharField(max_length=80, default="Commuter & Urban")
    Range = models.DecimalField(default=21, max_digits=4, decimal_places=0)

    def __unicode__(self):
        return self.name

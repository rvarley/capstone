from django.db import models


class Bike(models.Model):
    model = models.CharField(max_length=70)
    # Price = models.DecimalField(default=1501.00, max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    url = models.CharField(max_length=150)
    best_use = models.CharField(max_length=80, default="Commuter & Urban")
    b_range = models.CharField(max_length=20)

    def __unicode__(self):
        return self.model

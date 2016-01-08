from django.db import models


class Bike(models.Model):
    model = models.CharField(max_length=70)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    url = models.CharField(max_length=150)
    best_use = models.TextField(default="n/a")
    photo = models.TextField(default="n/a")
    b_range = models.CharField(max_length=6, default="n/a")
    assistance = models.CharField(max_length=50, default="n/a")
    motor = models.TextField(default="n/a")
    top_speed = models.CharField(max_length=6, default="n/a")
    weight = models.CharField(max_length=12, default="n/a")
    brakes = models.TextField(default="n/a")
    battery = models.TextField(default="n/a")

    def __unicode__(self):
        # return self.model
        return '%s %s' % (self.model, self.best_use)
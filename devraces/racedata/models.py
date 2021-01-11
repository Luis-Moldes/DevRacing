from django.db import models

# Create your models here.

from django.db import models



class Pilot(models.Model):

    name = models.CharField(max_length=100, blank=True, default='')
    idcode = models.CharField(max_length=100, blank=True, default='', unique=True)
    picture = models.URLField(max_length=100, blank=True, default='')
    age = models.IntegerField(default=0)
    team = models.CharField(max_length=100, blank=True, default='')
    races = models.TextField(default='', unique=True)
    total_pts = models.IntegerField(default=0)
    total_time = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        unique_together = ["id"]
        ordering = ['-total_pts']
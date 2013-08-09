from django.db import models
from django.contrib.auth.models import User

class RawFractal(models.Model):
    author = models.ForeignKey(User)
    rawfractimg = models.CharField(max_length=40)
    size = models.IntegerField(default=0)
    roughness = models.DecimalField(max_digits=2, decimal_places=1)
    perturbance = models.DecimalField(max_digits=2, decimal_places=1)


class Fractal(models.Model):
    author = models.ForeignKey(User)
    pub_date = models.DateTimeField('date created', auto_now=True)
    fractalimg = models.CharField(max_length=40)
    title = models.CharField(max_length=40)
    likes = models.IntegerField(default=0)
    rawfractal = models.ForeignKey(RawFractal)
    useheat = models.BooleanField()

    def __unicode__(self):
        return self.title


class Filter(models.Model):
    fractal = models.ForeignKey(Fractal)
    X1 = models.IntegerField(default=0)
    Y1 = models.IntegerField(default=0)
    sigX1 = models.DecimalField(max_digits=3, decimal_places=2)
    sigY1 = models.DecimalField(max_digits=3, decimal_places=2)

class ColorStop(models.Model):
    fractal = models.ForeignKey(Fractal)
    color = models.CharField(max_length=8)
    stop = models.IntegerField(default=0)
    
class Comment(models.Model):
    author = models.ForeignKey(User)
    body = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now=True)
    fractal = models.ForeignKey(Fractal)


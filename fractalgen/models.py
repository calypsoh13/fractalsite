from django.db import models
from django.contrib.auth.models import User

class RawFractal(models.Model):
    author = models.ForeignKey(User)
    rawFractImg = models.CharField(max_length=255)
    rawFractFile = models.CharField(max_length=255)
    size = models.IntegerField(default=257)
    sizeSetting = models.IntegerField(default=8)
    roughness = models.DecimalField(max_digits=2, decimal_places=1)
    roughnessSetting = models.IntegerField(default=5)
    perturbance = models.DecimalField(max_digits=2, decimal_places=1)
    perturbanceSetting = models.IntegerField(default=5)


class Fractal(models.Model):
    author = models.ForeignKey(User)
    pubDate = models.DateTimeField('date created', auto_now=True)
    fractalImg = models.CharField(max_length=40)
    title = models.CharField(max_length=40)
    rawFractal = models.ForeignKey(RawFractal)
    useHeat = models.BooleanField()

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
    useStop = models.BooleanField()
    optional = models.BooleanField()
    
class Comment(models.Model):
    author = models.ForeignKey(User)
    body = models.TextField()
    pubDate = models.DateTimeField('date published', auto_now=True)
    fractal = models.ForeignKey(Fractal)

class Like(models.Model):
    liker = models.ForeignKey(User)
    fractal = models.ForeignKey(Fractal)

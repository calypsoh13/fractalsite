from django.db import models
from django.contrib.auth.models import User
from fractalgen.calc import plasma, pngsaver
from django.core.files import File
import os
import numpy
import time
from django.conf import settings
import logging

# For debugging
logger = logging.getLogger('fractalsite.fractalgen.stuff')


def tmpMatrixTxt(matrix, self):
    """
    Save a matrix to a file.

    Generates a filename to save to and returns that filename.
    """
    matrixfilename = "static/img/matrixfiles/tmp-" + str(self.author) + "-" + time.strftime("%Y%m%d-%H%M%S") + ".txt"
    numpy.savetxt(matrixfilename, matrix)
    return matrixfilename

def tmpPreviewImage(matrix, self):
    """
    Save a preview image as a png.

    Generates a filename to save to and returns that filename.
    """
    imagefilename = "static/img/previewfiles/tmp-" + str(self.author) + "-" + time.strftime("%Y%m%d-%H%M%S") + ".png"
    pngsaver.createPreview(imagefilename, matrix, 129)
    return imagefilename

class RawFractal(models.Model):
    author = models.ForeignKey(User)
    rawFractImg = models.FileField(blank=True, null=True, upload_to='img/previewfiles')
    rawFractFile = models.FileField(blank=True, null=True, upload_to='img/matrixfiles')
    size = models.IntegerField(default=257)
    sizeSetting = models.IntegerField(default=8)
    roughness = models.FloatField()
    roughnessSetting = models.IntegerField(default=5)
    perturbance = models.FloatField()
    perturbanceSetting = models.IntegerField(default=5)
    
    def save(self, *args, **kwargs):
        """
        Override RawFractal's save() method

        Generates matrix with the instance's size, roughness and perturbance.
        Populates rawFractFile and RawFractImg fields with filepaths.
        """
        logger.info(self.author) # See who the author is
        
        matrix = plasma.diamondSquareTileableFractal(self.size, self.roughness, self.perturbance)

        tmpmatrixpath = tmpMatrixTxt(matrix, self)
        with open(tmpmatrixpath) as f:
            self.rawFractFile.save((str(self.author) + "-" + time.strftime("%Y%m%d-%H%M%S") + ".txt"), File(f), save=False)
        os.remove(tmpmatrixpath)

        tmpimagepath = tmpPreviewImage(matrix, self)
        with open(tmpimagepath) as f:
            self.rawFractImg.save((str(self.author) + "-" + time.strftime("%Y%m%d-%H%M%S") + ".png"), File(f), save=False)
        os.remove(tmpimagepath)
        
        super(RawFractal, self).save(*args, **kwargs)

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
    X = models.IntegerField(default=0)
    Y = models.IntegerField(default=0)
    xSetting = models.IntegerField(default = 0)
    ySetting = models.IntegerField(default = 0)
    sigmaX = models.DecimalField(max_digits=3, decimal_places=2)
    sigmaY = models.DecimalField(max_digits=3, decimal_places=2)
    sigmaXSetting = models.IntegerField(default = 0)
    sigmaYSetting = models.IntegerField(default = 0)

class ColorStop(models.Model):
    fractal = models.ForeignKey(Fractal)
    color = models.CharField(max_length=8)
    stop = models.IntegerField(default=0)
    optional = models.BooleanField()
    useStop = models.BooleanField()
    
class Comment(models.Model):
    author = models.ForeignKey(User)
    body = models.TextField()
    pubDate = models.DateTimeField('date published', auto_now=True)
    fractal = models.ForeignKey(Fractal)

class Like(models.Model):
    author = models.ForeignKey(User)
    fractal = models.ForeignKey(Fractal)


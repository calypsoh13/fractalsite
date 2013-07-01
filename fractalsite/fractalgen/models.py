from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from time import time

def get_upload_filename(instance, filename):
    f = filename.split('/')[-1]
    return "images/uploaded_files/%s" % (f)
            
class Fractal(models.Model):
    # Fields entered programatically
    author = models.ForeignKey(User)
    pub_date = models.DateTimeField('date created', auto_now=True)
    fractalimg = models.FileField(upload_to=get_upload_filename)
    # Fields entered in form by user
    title = models.CharField(max_length=40)
    # Fields updated later by other users
    likes = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(User)
    body = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now=True)
    fractal = models.ForeignKey(Fractal)


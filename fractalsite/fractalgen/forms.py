from django import forms
from models import Fractal, Comment
from django.core.validators import MaxValueValidator, MinValueValidator


class GenerateFractalForm(forms.Form):

    # Some choices for our fields
    FILTER_CHOICES = (('gaussian', 'gaussian'), ('other', 'other'))
    COLORTYPE_CHOICES = (('heat', 'heat'), ('gradient', 'gradient'))
    
    size = forms.IntegerField(validators = [MinValueValidator(0), MaxValueValidator(2000)])
    roughness = forms.FloatField(validators = [MinValueValidator(0), MaxValueValidator(1)])
    perturbance = forms.FloatField(validators = [MinValueValidator(0), MaxValueValidator(1)])

    filtertype = forms.ChoiceField(choices=FILTER_CHOICES)
    filterx = forms.IntegerField(validators = [MinValueValidator(0), MaxValueValidator(2000)])
    filtery = forms.IntegerField(validators = [MinValueValidator(0), MaxValueValidator(2000)])
    sigx = forms.IntegerField(validators = [MinValueValidator(0), MaxValueValidator(20)])
    sigy = forms.IntegerField(validators = [MinValueValidator(0), MaxValueValidator(20)])
    
    # Maybe make form dynamic and show colors if gradiant is selected? Sounds like javascript work in the template.
    colortype = forms.TypedChoiceField(choices=COLORTYPE_CHOICES, coerce=str)
    # There might be a better way to get input about colors, but this is fine for now...
    color1R = forms.IntegerField(validators = [MinValueValidator(0), MaxValueValidator(255)], required=False)
    color1G = forms.IntegerField(validators = [MinValueValidator(0), MaxValueValidator(255)], required=False)
    color1B = forms.IntegerField(validators = [MinValueValidator(0), MaxValueValidator(255)], required=False)
    color2R = forms.IntegerField(validators = [MinValueValidator(0), MaxValueValidator(255)], required=False)
    color2G = forms.IntegerField(validators = [MinValueValidator(0), MaxValueValidator(255)], required=False)
    color2B = forms.IntegerField(validators = [MinValueValidator(0), MaxValueValidator(255)], required=False)

class FractalForm(forms.ModelForm):

    class Meta:
        model = Fractal
        fields = ('title',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('body',)

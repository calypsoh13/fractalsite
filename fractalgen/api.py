from tastypie.resources import ModelResource
from fractalgen.models import Fractal

class FractalResource(ModelResource):
    class Meta:
        queryset = Fractal.objects.all()
        resource_name = 'fractal'

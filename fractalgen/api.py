from tastypie.resources import ModelResource
from fractalgen.models import Matrix, Fractal, Filter, ColorStop
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from django.contrib.auth.models import User
from tastypie import fields
from django.core.serializers import json
from django.utils import simplejson
from tastypie.serializers import Serializer
import logging

logger = logging.getLogger('fractalsite.fractalgen.stuff')


class PrettyJSONSerializer(Serializer): 
    json_indent = 4 
 
    def to_json(self, data, options=None): 
        options = options or {} 
        data = self.to_simple(data, options) 
        return simplejson.dumps(data, cls=json.DjangoJSONEncoder, sort_keys=True, ensure_ascii=False, indent=self.json_indent) 
 

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        serializer = PrettyJSONSerializer()
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True

class MatrixResource(ModelResource):
    author = fields.ForeignKey(UserResource, 'author')

    class Meta:
        queryset = Matrix.objects.all()
        resource_name = 'matrix'
        serializer = PrettyJSONSerializer()
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True

    def hydrate_author(self, bundle):
        logger.info(bundle.request.user.is_anonymous())
        if bundle.request.user.is_anonymous():
            bundle.data['author'] = User.objects.get(username = 'guest')
        else:
            bundle.data['author'] = User.objects.get(pk = bundle.request.user.pk)
        return bundle

class FractalResource(ModelResource):
    matrix = fields.ForeignKey(MatrixResource, 'matrix')
    class Meta:
        queryset = Fractal.objects.all()
        resource_name = 'fractal'
        serializer = PrettyJSONSerializer()
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True

    def hydrate_matrix(self, bundle):
        logger.info(bundle.data['matix'])
        x = bundle.data['matrix']
        


class FilterResource(ModelResource):
    fractal = fields.ForeignKey(FractalResource, 'fractal')
    class Meta:
        queryset = Filter.objects.all()
        resource_name = 'filter'
        serializer = PrettyJSONSerializer()
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True

class ColorStopResource(ModelResource):
    fractal = fields.ForeignKey(FractalResource, 'fractal')
    class Meta:
        queryset = ColorStop.objects.all()
        resource_name = 'colorstop'
        serializer = PrettyJSONSerializer()
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True

from tastypie.resources import ModelResource
from fractalgen.models import Matrix
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from django.contrib.auth.models import User
from tastypie import fields
from django.core.serializers import json
from django.utils import simplejson
from tastypie.serializers import Serializer


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
        bundle.data['author'] = User.objects.get(pk = bundle.request.user.pk)
        return bundle


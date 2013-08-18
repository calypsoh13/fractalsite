from tastypie.resources import ModelResource
from fractalgen.models import RawFractal
from tastypie.authorization import Authorization
from django.contrib.auth.models import User
from tastypie import fields

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        default_format = 'application/json'

class RawFractalResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = RawFractal.objects.all()
        resource_name = 'rawfractal'
        default_format = 'application/json'
        authorization = Authorization()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get']
        always_return_data = True

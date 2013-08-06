from django.shortcuts import render_to_response
from fractalgen.models import Fractal
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf

def create(request):
    return render_to_response('index.html')


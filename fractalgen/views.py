from django.shortcuts import render_to_response
from fractalgen.models import Fractal
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.context_processors import csrf

def fractalapp(request):
    return render_to_response('index.html', context_instance=RequestContext(request))

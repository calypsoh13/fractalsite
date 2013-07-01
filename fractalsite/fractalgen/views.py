from django.shortcuts import render_to_response
from fractalgen.models import Fractal
from django.http import HttpResponse, HttpResponseRedirect
from forms import GenerateFractalForm, FractalForm, CommentForm
from django.core.context_processors import csrf
from django.core.files import File
import uuid
from time import time
import plasma
import pngsaver
import numpy
import os

def get_fileloc(title, filetype):
    return "static/images/tmp/%s_%s.%s" % (str(time()).replace('.','_'), title.replace(' ','_'), str(filetype))

def filterMatrix(matrix, size, x, y, sigx, sigy):
    fractalfilter = plasma.gaussianFilter(size, [[x, y, sigx, sigy]])
    return numpy.multiply(matrix, fractalfilter)

def fractals(request):
    args = {}
    args.update(csrf(request))

    args['fractals'] = Fractal.objects.all()
    
    return render_to_response('fractals.html', args)

def fractal(request, fractal_id=1):
    return render_to_response('fractal.html', {'fractal': Fractal.objects.get(id=fractal_id) })

def like_fractal(request, fractal_id):
    if fractal_id:
        frac = Fractal.objects.get(id=fractal_id)
        frac.likes += 1
        frac.save()
    return HttpResponseRedirect('/fractals/get/%s' % fractal_id)

def add_comment(request, fractal_id):
    frac = Fractal.objects.get(id=fractal_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            cmt = form.save(commit=False)
            cmt.author = request.user
            cmt.fractal = frac
            cmt.save()

            return HttpResponseRedirect('/fractals/get/%s' % fractal_id)
    else:
        form = CommentForm()

    args = {}
    args.update(csrf(request))

    args['fractal'] = frac
    args['form'] = form

    return render_to_response('add_comment.html', args)

def create(request):
    if request.POST:
        form = GenerateFractalForm(request.POST)
        if form.is_valid():
            matrix = plasma.diamondSquareFractal(size=form.cleaned_data['size'], roughness=form.cleaned_data['roughness'], perturbance=form.cleaned_data['perturbance'])
            matrix = filterMatrix(matrix, size=form.cleaned_data['size'], x=form.cleaned_data['filterx'], y=form.cleaned_data['filtery'], sigx=form.cleaned_data['sigx'], sigy=form.cleaned_data['sigy'])
            fileloc = "images/tmp/%s.png" % (uuid.uuid4())
            saveto = "static/" + fileloc
            if str(form.cleaned_data['colortype']) == 'heat':
                pngsaver.saveHeat(saveto, matrix)
            elif str(form.cleaned_data['colortype']) == 'gradient':
                fromcolor = [form.cleaned_data['color1R'], form.cleaned_data['color1G'], form.cleaned_data['color1B']]
                tocolor = [form.cleaned_data['color2R'], form.cleaned_data['color2G'], form.cleaned_data['color2B']]
                pngsaver.saveGradient(saveto, matrix, fromcolor, tocolor)
            response = HttpResponseRedirect('/fractals/save')
            response.set_cookie('fileloc', fileloc)
            return response
    else:
        form = GenerateFractalForm()
    
    args = {}
    args.update(csrf(request))

    args['form'] = form

    return render_to_response('create_fractal.html', args)


def save(request):
    if 'fileloc' in request.COOKIES:
        fileloc = request.COOKIES['fileloc']
        tmpfile = "static/" + fileloc
    if request.POST:
        form = FractalForm(request.POST)
        if form.is_valid():
            frac = form.save(commit=False)
            frac.author = request.user
            frac.title = form.cleaned_data['title']
            newfilename = "%s_%s.png" % (str(time()).replace('.','_'), (str(form.cleaned_data['title'])).replace(' ','_'))
            with open(tmpfile, 'rb') as frac_file:
                frac.fractalimg.save(newfilename, File(frac_file), save=False)
            os.remove(tmpfile)
            frac.save()

            return HttpResponseRedirect('/fractals/all')

    else:
        form = FractalForm()
    
    args = {}
    args.update(csrf(request))

    args['form'] = form
    args['fileloc'] = fileloc

    return render_to_response('save_fractal.html', args)


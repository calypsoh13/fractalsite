from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
        url(r'^$', 'fractalgen.views.fractals'),
        url(r'^(?P<fractal_id>\d+)/$', 'fractalgen.views.fractal'),
        url(r'^create/$', 'fractalgen.views.create'),
        url(r'^save/$', 'fractalgen.views.save'),
        url(r'^like/(?P<fractal_id>\d+)/$', 'fractalgen.views.like_fractal'),
        url(r'^add_comment/(?P<fractal_id>\d+)/$', 'fractalgen.views.add_comment'),

        )



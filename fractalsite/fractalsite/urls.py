from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fractalsite.views.home', name='home'),
    # url(r'^fractalsite/', include('fractalsite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^fractals/', include('fractalgen.urls')),
    (r'^fractal/', include('fractalgen.urls')),
    url(r'^/$', 'fractalsite.views.welcome'),
    url(r'^$', 'fractalsite.views.welcome'),
    # Logging in
    url(r'^accounts/login/$', 'fractalsite.views.login'),
    url(r'^accounts/auth/$', 'fractalsite.views.auth_view'),
    url(r'^accounts/logout/$', 'fractalsite.views.logout'),
    url(r'^accounts/loggedin/$', 'fractalsite.views.loggedin'),
    url(r'^accounts/invalid/$', 'fractalsite.views.invalid_login'),
    # Registering
    url(r'^accounts/register/$', 'fractalsite.views.register_user'),
    url(r'^accounts/register_success/$', 'fractalsite.views.register_success'),

)

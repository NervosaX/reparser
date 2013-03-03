from django.conf.urls import patterns, include, url
from django.contrib import admin

from base import views as base_views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', base_views.Index.as_view(), name='index'),
    # url(r'^rescrape/', include('rescrape.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)


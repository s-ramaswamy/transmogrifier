from django.conf.urls.defaults import patterns, url, include
from django.contrib            import admin
from messportal import urls

admin.autodiscover()

urlpatterns = patterns('',

        url(r'^admin/',
            include(admin.site.urls)
            ),

        url(r'^',
            include('transmogrifier.messportal.urls')
            ),
        )

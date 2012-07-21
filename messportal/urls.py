from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('Transmogrifier.messportal.views',
    # Form to register for a mess caterer
    url(
        r'^register/$',
        'register',
        name = 'register',
    ),
    
    # Success message on completion of registration
    url(
        r'^registration_success/(?P<caterer>.*)/$',
        'registration_success',
        name = 'registration_success',
    ),
)

#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from messportal.models import *
from messportal.forms import RegistrationForm


@csrf_exempt
def register(request):
    """
    View to deal with mess registration by users.
    """

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():

            # Authorization and authentication is done in the form
            # TODO: cleaning of feedback
            # TODO: cleaning of caterer

            # Update the UserProfile with the feedback and choice of caterer

            data = form.cleaned_data
            user = data['user']
            user.profile.feedback = int(data['feedback_hygeine']
                    + data['feedback_quality']
                    + data['feedback_quantity'])
            user.profile.save()
            Caterer = data['Caterer']
            caterer_object = Caterer(user=user)
            caterer_object.save()
            return redirect('registration_success', Caterer.__name__)
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render_to_response('messportal/register.html', context,
                              context_instance=RequestContext(request))


def registration_success(request, caterer):
    """
    View to give a success message after registration is complete.
    """

    context = {'caterer': caterer}

    # Purposely not using RequestContext here, because it pings the db.

    return render_to_response('messportal/registration_success.html',
                              context,
                              context_instance=RequestContext(request))



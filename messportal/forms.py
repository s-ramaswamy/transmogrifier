#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.db.models.base import ModelBase

from transmogrifier.messportal import models
from transmogrifier.messportal.models import UserProfile, \
    AbstractMessTuple

FEEDBACK_CHOICES = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5'
                    , '5'))

MESS_CHOICES = (
    ('Cauvery', 'Cauvery'),
    ('Krishna', 'Krishna'),
    ('HimalayaGF', 'HimalayaGF'),
    ('Himalaya1F', 'Himalaya1F'),
    ('Himalaya2F', 'Himalaya2F'),
    ('Mandakini', 'Mandakini'),
    )


def get_list_of_caterers():
    list_of_caterers = []
    for obj in models.__dict__.values():
        if not isinstance(obj, ModelBase):
            continue
        if obj.__base__ != AbstractMessTuple:
            continue
        if obj == AbstractMessTuple:
            continue
        Model = obj
        limit = getattr(models, Model.__name__ + '_LIMIT')
        if Model.objects.count() < limit:
            list_of_caterers.append((Model.__name__, Model.__name__))
    return list_of_caterers


class HorizontalRadioRenderer(forms.RadioSelect.renderer):

    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class HorizontalRadioSelect(forms.RadioSelect):

    renderer = HorizontalRadioRenderer


class RegistrationForm(forms.Form):

    """
    Form for users to provide feedback register for a mess.
    """

    # User authentication

    username = forms.CharField(help_text='Roll number')
    password = forms.CharField(widget=forms.PasswordInput(),
                               help_text='Password')

    # Feedback

    feedback_hygeine = \
        forms.CharField(widget=HorizontalRadioSelect(choices=FEEDBACK_CHOICES))
    feedback_quality = \
        forms.CharField(widget=HorizontalRadioSelect(choices=FEEDBACK_CHOICES))
    feedback_quantity = \
        forms.CharField(widget=HorizontalRadioSelect(choices=FEEDBACK_CHOICES))

    # New choice

    choice_of_caterer = \
        forms.ChoiceField(choices=get_list_of_caterers(),
                          widget=forms.RadioSelect)

    def clean(self):
        data = self.cleaned_data
        if 'username' in data and 'password' in data:
            try:

                # Try to get user and profile (authorization)

                user = User.objects.select_related('profile'
                        ).get(username=data['username'])

                # Check password (authentication)

                if not user.check_password(data['password']):
                    raise User.DoesNotExist
            except (User.DoesNotExist, UserProfile.DoesNotExist):
                raise forms.ValidationError('This username and password combination does not exist'
                        )

            # Check whether or not the user has already registered

            if user.profile.registered == True:
                raise forms.ValidationError('You have already registered. You cannot register again'
                        )

            # Add this user and profile object to cleaned_data to avoid
            # hitting the database again

            if 'choice_of_caterer' in data:
                Caterer = getattr(models, data['choice_of_caterer'])
                limit = getattr(models, data['choice_of_caterer']
                                + '_LIMIT')
                if Caterer.objects.count() < limit:
                    self.cleaned_data['user'] = user
                    self.cleaned_data['Caterer'] = Caterer
                else:
                    raise forms.ValidationError('This mess has already reached its limit. Try registering again'
                            )

        return data



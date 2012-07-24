from django.template                import RequestContext
from django.shortcuts               import render_to_response, redirect
from django.contrib.auth.models     import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf   import csrf_exempt
from django                         import forms

from messportal.models  import *
from messportal.forms   import RegistrationForm

Cauvery_LIMIT = 10
Krishna_LIMIT = 10
HimalayaGF_LIMIT = 10
Himalaya1F_LIMIT = 10
Himalaya2F_LIMIT = 10
Mandakini_LIMIT = 10

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
            if 'username' in data and 'password' in data:
                try:
                    # Try to get user and profile (authorization)
                    user = User.objects.select_related('profile').get(
                               username= data['username']
                           )
                    # Check password (authentication)
                    if not user.check_password(data['password']):
                        raise User.DoesNotExist
                except (User.DoesNotExist, UserProfile.DoesNotExist):
                    raise forms.ValidationError("This username and password"
                                                "combination does not exist")
                # Add this user and profile object to cleaned_data to avoid
                # hitting the database again
                if user.profile.registered == True:
                    raise forms.ValidationError("You have already registered."
                                                " You cannot register again"  )
                user.profile.feedback = int( data['feedback_hygeine'] +
                                             data['feedback_quality'] +
                                             data['feedback_quantity']  )
                
                if 'choice_of_caterer' in data:
                    caterer = eval( data['choice_of_caterer'] )
                    limit = eval( data['choice_of_caterer'] + '_LIMIT' )
                    if caterer.objects.count() < limit:
                        caterer_object = caterer(user=user)
                        caterer_object.save()
                        user.profile.registered = True
                        user.profile.save()
                        return redirect( 'registration_success', 
                                         data['choice_of_caterer'] )
                    else:
                        raise forms.ValidationError("This mess has already "
                                                    "reached its limit"     )
    else:
        form = RegistrationForm()
    
    context = { 'form': form, }
    return render_to_response('messportal/register.html', context,
                              context_instance = RequestContext(request))

def registration_success(request, caterer):
    """
    View to give a success message after registration is complete.
    """
    
    context = { 'caterer': caterer, }
    # Purposely not using RequestContext here, because it pings the db.
    return render_to_response('messportal/registration_success.html', context,
                              context_instance = RequestContext(request)      )


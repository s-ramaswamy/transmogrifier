from django.template                import RequestContext
from django.shortcuts               import render_to_response, redirect
from django.contrib.auth.models     import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf   import csrf_exempt

from messportal.models  import *
from messportal.forms   import RegistrationForm

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
                    user = User.objects.select_related('profile').get(username= data['username'])
                    # Check password (authentication)
                    if not user.check_password(data['password']):
                        raise User.DoesNotExist
                except (User.DoesNotExist, UserProfile.DoesNotExist):
                    raise forms.ValidationError("This username and password"
                                            "combination does not exist")
                # Add this user and profile object to cleaned_data to avoid
                # hitting the database again
                user.profile.feedback = int(data['feedback_hygeine']+data['feedback_quality']+data['feedback_quantity'])
                user.profile.save()
                caterer = eval(data['choice_of_caterer'])
                caterer_object = caterer(user=user)
                caterer_object.save()
                return redirect('registration_success', data['choice_of_caterer'])
    else:
        form = RegistrationForm()
    
    context = { 'form': form, }
    # Purposely not using RequestContext here, because it pings the db.
    return render_to_response('messportal/register.html', context)


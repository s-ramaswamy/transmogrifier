from django.template                import RequestContext
from django.shortcuts               import render_to_response, redirect
from django.contrib.auth.models     import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf   import csrf_exempt

from messportal.models  import UserProfile
from messportal.models  import get_caterer_id, get_caterer_name
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
                user.profile.choice_of_caterer_id = int(get_caterer_id(data['choice_of_caterer']))
                user.profile.save()
            
                return redirect('registration_success', get_caterer_name(
                    data['choice_of_caterer']))
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
                              context_instance = RequestContext(request))


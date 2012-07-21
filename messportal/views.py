from django.template                import RequestContext
from django.shortcuts               import render_to_response, redirect
from django.contrib.auth.models     import User
from django.contrib.auth.decorators import login_required

from messportal.models  import UserProfile, get_object_from_choice
from messportal.models  import get_caterer_id, get_caterer_name
from messportal.forms   import RegistrationForm

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
            user = form.cleaned_data['user']
            user.profile.feedback = form.cleaned_data['feedback']
            user.profile.choice_of_caterer = get_caterer_id(
                form.cleaned_data['choice_of_caterer']
            )
            user.profile.save()
            
            return redirect('registration_success', get_caterer_name(
                form.cleaned_data['choice_of_caterer']
            ))
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
    return render_to_response('messportal/registration_success.html', context,
                              context_instance = RequestContext(request))


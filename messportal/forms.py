from django                     import forms
from django.contrib.auth.models import User

from messportal.models      import UserProfile, get_list_of_caterers

class RegistrationForm(forms.Form):
    """
    Form for users to provide feedback register for a mess.
    """
    # User authentication
    username = forms.CharField(help_text = "Roll number")
    password = forms.CharField(widget = forms.PasswordInput(), 
                               help_text = "Password")
    
    # Feedback
    # Javascript will do the job of encoding
    feedback = forms.IntegerField()
    
    # New choice
    choice_of_caterer = forms.ChoiceField(choices = get_list_of_caterers())
    
    def clean(self):
        """
        Perform validation of username and password.
        """
        data = self.cleaned_data
        if 'username' in data and 'password' in data:
            try:
                # Try to get user and profile (authorization)
                user = User.objects.select_related(
                                        'profile'
                                    ).get(
                                        username = data['username']
                                    )
                # Check password (authentication)
                if not user.check_password(data['password']):
                    raise User.DoesNotExist
            except (User.DoesNotExist, UserProfile.DoesNotExist):
                raise forms.ValidationError("This username and password"
                                            "combination does not exist")
            # Add this user and profile object to cleaned_data to avoid
            # hitting the database again
            self.cleaned_data['user'] = user
    
    # Cleaning of remaining fields will be carried out in the view

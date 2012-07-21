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
     # Cleaning of remaining fields will be carried out in the view

from django                 import forms
from messportal.models      import get_list_of_caterers

class RegistrationForm(forms.Form):
    # User authentication
    username = forms.CharField(help_text = "Roll number")
    password = forms.CharField(widget = forms.PasswordInput(), 
                               help_text = "Password")
    
    # Feedback
    # Javascript will do the job of encoding
    feedback = forms.IntegerField()
    
    # New choice
    choice_of_caterer = forms.ChoiceField(choices = get_list_of_caterers())
    
    # Form cleaning will be carried out in the view            

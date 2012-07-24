from django                     import forms
from django.contrib.auth.models import User
from django.utils.safestring    import mark_safe

from messportal.models      import UserProfile

FEEDBACK_CHOICES = (('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),)
MESS_CHOICES = (('Cauvery','Cauvery'),('Krishna','Krishna'),('HimalayaGF','HimalayaGF'),('Himalaya1F','Himalaya1F'),('Himalaya2F','Himalaya2F'),('Mandakini','Mandakini'),)
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
    username = forms.CharField(help_text = "Roll number")
    password = forms.CharField(widget = forms.PasswordInput(), 
                               help_text = "Password")
    
    # Feedback
    # Javascript will do the job of encoding
    feedback_hygeine = forms.CharField(widget = HorizontalRadioSelect(choices = FEEDBACK_CHOICES))
    feedback_quality = forms.CharField(widget = HorizontalRadioSelect(choices = FEEDBACK_CHOICES))
    feedback_quantity = forms.CharField(widget = HorizontalRadioSelect(choices = FEEDBACK_CHOICES))
    #New choice
    choice_of_caterer = forms.ChoiceField(choices = MESS_CHOICES, widget=forms.RadioSelect)


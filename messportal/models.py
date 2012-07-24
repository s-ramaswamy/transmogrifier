from django.db                      import models
from django.contrib.auth.models     import User

class UserProfile(models.Model):
    """
    Model to contain feedback information of previous mess experience.
    """
    # This must be 1-2-1 and not FK so that select_related works in the form
    user = models.OneToOneField(User, related_name = 'profile')
    
    # Rating for each feedback field is encoded into a single integer field
    # For example:
    #       Hygiene   - 3
    #       Quantity  - 4
    #       Quality   - 3
    #       Overall   - 3
    # will be encoded as 3433
    feedback = models.IntegerField(blank = False, null = True)
    registered = models.BooleanField(default = False) 
    def __unicode__(self):
        return unicode(self.user)

class AbstractMessTuple(models.Model):
    """
    Abstract mess model from which all the different messes inherit.
    """
    user = models.ForeignKey(User, related_name = 'choice', unique = True)

    def __unicode__(self):
        return unicode(self.user.username)

class Cauvery(AbstractMessTuple):
    """
    Cauvery
    """
class Krishna(AbstractMessTuple):
    """
    Krishna
    """
class HimalayaGF(AbstractMessTuple):
    """
    Himalaya Ground Floor
    """
class Himalaya1F(AbstractMessTuple):
    """
    Himalaya First Floor
    """
class Himalaya2F(AbstractMessTuple):
    """
    Himalays Second Floor
    """
class Mandakini(AbstractMessTuple):
    """
    Mandakini
    """

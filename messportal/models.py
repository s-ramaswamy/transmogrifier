from django.db                      import models
from django.contrib.auth.models     import User

class UserProfile(models.Model):
    """
    Model to contain feedback information of previous mess experience.
    Also contains current caterer choice.
    """
    user = models.ForeignKey(User)
    
    # Rating for each feedback field is encoded into a single integer field
    # For example:
    #       Hygiene   - 3
    #       Quantity  - 4
    #       Quality   - 3
    #       Overall   - 3
    # will be encoded as 3433
    feedback = models.IntegerField(blank = False, null = True)
    
    choice_of_caterer = models.ForeignKey(Caterer)
    
    def __unicode__(self):
        return unicode(user)


class Caterer(models.Model):
    """
    Model to contain caterer information. Records of this table make up the 
    choices for users to select from.
    """
    name = models.CharField(max_length = 100)
    
    def __unicode__(self):
        return unicode(self.name)


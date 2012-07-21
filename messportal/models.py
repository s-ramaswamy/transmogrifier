from django.db                      import models
from django.contrib.auth.models     import User

class UserProfile(models.Model):
    """
    Model to contain feedback information of previous mess experience.
    Also contains current caterer choice.
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
    
    choice_of_caterer = models.ForeignKey(Caterer, related_name = 'students')
    
    def __unicode__(self):
        return unicode(user)


class Caterer(models.Model):
    """
    Model to contain caterer information. Records of this table make up the 
    choices for users to select from.
    """
    name = models.CharField(max_length = 100)
    limit = models.IntegerField()
    # 'students' is a related field - FK from UserProfile
    
    def __unicode__(self):
        return unicode(self.name)


CATERER_ID_MANGLER = u'|'


def get_list_of_caterers():
    """
    Returns a list of caterers for the current implementaton.
    This list will be displayed directly on the template, therefore it must
    pass basic tests such as limit-checking.
    """
    list_of_caterers = []
    for caterer in Caterer.objects.all():
        # Check if number of students registered already is less than limit
        if caterer.limit > caterer.students.count():
            # Mangle the name and id of the caterer into a single string
            # so that the view can later use both without having to query
            # the database
            mangled_caterer_id = unicode(caterer.id) + CATERER_ID_MANGLER + \
                                 unicode(caterer.name)
            list_of_caterers.append( (mangled_caterer_id, caterer.name) )
    return list_of_caterers


def get_caterer_id(mangled_caterer_id):
    """
    Unmangles the caterer-id-and-name and returns the id alone.
    """
    
    return mangled_caterer_id.split(CATERER_ID_MANGLER)[0]


def get_caterer_name(mangled_caterer_id):
    """
    Unmangles the caterer-id-and-name and returns the name alone.
    """
    
    return mangled_caterer_id.split(CATERER_ID_MANGLER)[1]


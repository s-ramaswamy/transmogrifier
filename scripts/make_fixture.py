from django.contrib.auth.models import User
u = User(username = 'xyz')
for i in range(1, 6001):
    print "- model: auth.User"
    print "  pk: %s" % i
    print "  fields:"
    print "    username: %s" % i
    print "    email: this@is.arbit"
    u.set_password(str(i))
    password = u.password
    print "    password: " + password
    print "- model: messportal.UserProfile"
    print "  pk: %s" % i
    print "  fields:"
    print "    user: %s" % i


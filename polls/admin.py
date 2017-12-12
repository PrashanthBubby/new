from django.contrib import admin
from polls.models import UserProfile,Posts,Onetimelinks

admin.site.register(UserProfile)
admin.site.register(Posts)
admin.site.register(Onetimelinks)

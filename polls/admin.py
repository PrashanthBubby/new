from django.contrib import admin
from polls.models import UserProfile,Posts,Onetimelinks,Comments,Requests,Likes

admin.site.register(UserProfile)
admin.site.register(Posts)
admin.site.register(Onetimelinks)
admin.site.register(Comments)
admin.site.register(Requests)
admin.site.register(Likes)
from django.conf.urls import url
#from django.contrib.auth.views import login
from django.contrib import admin

from .views import(
    PostListAPIView,
    UserLoginAPIView,
    PostUpdateAPIView,
    EmailSendingAPIView,
    ProfileListAPIView,
    ProfileEditAPIView,
    PostCreateAPIView,
    ProfileUpdateAPIView,
    EmailInviteAPIView,
    )

urlpatterns = [
    #url(r'^signup/', views.signup, name='signup'),
    #url(r'^signup_form/', views.signup_cr, name='signup'),
    url(r'^login/', UserLoginAPIView.as_view(),name='login'),
    url(r'^profile/$', ProfileListAPIView.as_view(), name='profile'),
    url(r'^edit/', ProfileEditAPIView.as_view(), name='edit_profile'),
    #url(r'^edit_profile/', views.edit_profile, name='profile'),
    url(r'^(?P<pk>\d+)/edit/$',ProfileUpdateAPIView.as_view(), name='update_profile'),
    url(r'^forgot/',EmailSendingAPIView.as_view() , name='forgot'),
    url(r'^invite/', EmailInviteAPIView.as_view(), name='forgot'),

    #end here#
    url(r'^create/',PostCreateAPIView.as_view(), name='lists'),
    url(r'^postsinapi/',PostListAPIView.as_view(), name='lists'),
    #url(r'^(?P<pk>\d+)$', views.DPostssss.as_view(), name='dposts'),
    #url(r'^followers/', views.followers, name='followers'),
    #url(r'^messages/', views.followers, name='messages'),
    #url(r'^tags/', views.followers, name='tags'),
    
    #url(r'^create_post/', views.createpost, name='createpost'),
    #url(r'^submit_post/', views.submit_post, name='createpost'),
]

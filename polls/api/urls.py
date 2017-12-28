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
    InviteOtherAPIView,
    RequestsListAPIView,
    SendRequestsAPIView,
    CommentsAPIView,
    CommentCreateAPIView,
	LikesAPIView,
	LikesCreateAPIView,
    )

urlpatterns = [
    url(r'^krigers/', SendRequestsAPIView.as_view(), name='signup'),
    url(r'^all_req/',RequestsListAPIView.as_view(), name='all_requests'),
    url(r'^login/', UserLoginAPIView.as_view(),name='login'),
    url(r'^profile/$', ProfileListAPIView.as_view(), name='profile'),
    url(r'^edit/', ProfileEditAPIView.as_view(), name='edit_profile'),
    url(r'^comments_view/', CommentsAPIView.as_view(), name='profile'),
    url(r'^(?P<pk>\d+)/edit/$',ProfileUpdateAPIView.as_view(), name='update_profile'),
    url(r'^forgot/',EmailSendingAPIView.as_view() , name='forgot'),
    url(r'^email_invite/', EmailInviteAPIView.as_view(), name='einvite'),
    url(r'^other_invite/', InviteOtherAPIView.as_view(), name='appinvite'),

    
    #end here#
    url(r'^create/',PostCreateAPIView.as_view(), name='lists'),
    url(r'^postsinapi/',PostListAPIView.as_view(), name='lists'),
    #url(r'^(?P<pk>\d+)$', views.DPostssss.as_view(), name='dposts'),
    url(r'^likes/', LikesAPIView.as_view(), name='like_a_post'),
    url(r'^like_post/', LikesCreateAPIView.as_view(), name='like_post'),
    #url(r'^tags/', views.followers, name='tags'),
    
    #url(r'^create_post/', views.createpost, name='createpost'),
    url(r'^comment/', CommentCreateAPIView.as_view(), name='make_comment'),
]

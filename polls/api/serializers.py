from rest_framework import serializers
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from polls.models import Posts,Onetimelinks,UserProfile,Requests,Comments,Likes #models
from django.db.models import Q
from rest_framework.fields import CurrentUserDefault

User=get_user_model()

class UserDetailSerializer(serializers.ModelSerializer):#User details
    class Meta:
        model=UserProfile
        fields=('first_name','last_name','image')
    
class PostSerializer(serializers.ModelSerializer):
    user_details=UserDetailSerializer(source='get_user_details',required=True,many=True)#nesting serializer
    class Meta:
        model=Posts
        fields=[
            'id',
			'title',
            'post',
            'date',
            'username',
            'user_details',
            'name',
            

            ]  
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Posts
        fields=[
            #'username',
            'title',
            'post',
            #'date',
            ]
class UserProfileSerializer(serializers.ModelSerializer):
    #follows = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('username',)
class ProfileSerializer(serializers.ModelSerializer):
    name=UserProfileSerializer(required=False,read_only=True)
    image=serializers.ImageField(label='profile_pic',required=False)
    school=serializers.CharField(label='school',required=False,allow_blank=True)
    college=serializers.CharField(label='college',required=False,allow_blank=True)
    highlight=serializers.CharField(label='highlights',required=False,allow_blank=True)
    subjects=serializers.CharField(label='subjects',required=False,allow_blank=True)
    stream=serializers.CharField(label='stream',required=False,allow_blank=True)
    projects=serializers.CharField(label='projects',required=False,allow_blank=True)
    internship=serializers.CharField(label='internship',required=False,allow_blank=True)
    phone=serializers.IntegerField(label='phone',required=False)
    class Meta:
        model=UserProfile
        fields=[
            'id',
            'name',
            'image',
            'first_name',
            'last_name',
            'school',
            'college',
            'highlight',
            'subjects',
            'stream',
            'projects',
            'internship',
            'phone',
            ]       
class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(label='Email Address',required=True,allow_blank=False)

    class Meta:
        model= User
        fields=[
            'email',
            'password'
            ]
        extra_kwargs={"password":{"write_only":True}}
    def validate(self,data):
        user_obj=None
        email=data.get("email",None)
        password=data.get("password")
        user=User.objects.filter(Q(email=email))
        if user.exists() and user.count()==1:
            user_obj=user.first()
        else:
            raise serializers.ValidationError("Email is not valid or not registered. Please enter correct email address")
        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError("Password is incorrect.please enter correct password")
        return data
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from time import time
from math import ceil,floor
from django.conf import settings
from django.core.mail import send_mail

class EmailSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(label='Email Address',required=True,allow_blank=False)
    class Meta:
        model=User
        fields=[
            'email'
            ]
    def validate(self,data):#validating the data
        user_obj=None
        email=data.get("email",None)
        user=User.objects.filter(Q(email=email))#getting the details of the email
        if user.exists() and user.count()==1:#if the email exists
            for user in user:
                user= user
                t=ceil(time())#timestsmp
                Onetimelinks.objects.filter(code=user.pk).delete()#if any email verifications are pending then the records will be deleted
                u=Onetimelinks(code=user.pk,token=t)#saving present details
                u.save()
                t=str(t).encode()#converting to byte
                subject='Reset link for password'#subject of a mail
                message = render_to_string('polls/password_resetlink_generation.html', {#joins the below contet asa a string 
                    'user': user,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),#encoding
                    'token':urlsafe_base64_encode(force_bytes(t)),#encoding
                    })
                    
                from_mail=settings.EMAIL_HOST_USER
                to_mail=[email]
                send_mail(subject,message,from_mail,to_mail,fail_silently=False)#sending mail
        else:
            raise serializers.ValidationError("Email is not registered or not valid")#if the email is not found returns error
        return data
class EmailInviteSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(label='Email Address',required=True)
    user= serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model=User
        fields=['email','user']
    def validate(self,data):
        user=data.get('user')
        email=data.get('email')
        subject='Join Kriger Campus'
        message = render_to_string('polls/email_invite.html', {
                    'user': user,
                    
                    })
        from_mail=settings.EMAIL_HOST_USER
        to_mail=[email]
        send_mail(subject,message,from_mail,to_mail,fail_silently=False)
        return data      
class OtherInviteSerializer(serializers.ModelSerializer):
    user= serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model=User
        fields=['user']
    def validate(self,data):
        user=data.get('user')
        return data
class RequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Requests
        fields=[
                'requested_to_id',
                'to_name',                
                ]
class SendRequestsSerializer(serializers.ModelSerializer):
    username=serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model=User
        fields=['username',
                'id',
                ]
class CommentsViewSerializer(serializers.ModelSerializer):
    #postdetails=PostSerializer(required=False,read_only=True)
    commenter_details=UserDetailSerializer(source='get_user_details',required=True,many=True)
    class Meta:
        model=Comments
        fields=[
                'commenter_id',
                'post',
                'commenter_name',
                'comment',
                'date',
                'commenter_details',
                ]
class CommentsSerializer(serializers.ModelSerializer):
    comments=CommentsViewSerializer(source='get_post_comments',many=True)
    post_by_details=UserDetailSerializer(source='get_user_details',required=True,many=True)
    class Meta:
        model=Posts
        fields=[
            'title',
            'post',
            'date',
            'username',
            'id',
            'name',
            'post_by_details',
            'comments',
            ]

class CommentCreateSerializer(serializers.ModelSerializer):
    comment=serializers.CharField()
    #commenter_details=UserDetail
    class Meta:
        model=Comments
        fields=[
            'post',
            'comment',
            ]
class LikesSerializer(serializers.ModelSerializer):
	liked_post=serializers.PrimaryKeyRelatedField(queryset=Posts.objects.all())
	class Meta:
		model=Likes
		fields=['liked_post']

"""
class LikesSerializer(serializers.ModelSerializer):
    user_details=UserDetailSerializer(source='get_details',many=True)
    class Meta:
        model=Likes
        fields=['liked_by','user_details']


class OwnPostsSerializer(serializers.ModelSerializer):
    likes=LikesSerializer(source='get_likes',many=True)
    class Meta:
        model=Posts
        fields=['id','title','post','date','likes']
"""
class PostLikesSerializer(serializers.ModelSerializer):
    owner=UserDetailSerializer(source='get_owner',many=True)
    class Meta:
        model=Posts
        fields=[
            #'username',
            'owner',
            'title',
            'post',
            #'date',
            ]
class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Likes
        fields=['liked_post']
class LikedSerializer(serializers.ModelSerializer):
    post_details=PostLikesSerializer(source='get_details',many=True)
    class Meta:
        model=Likes
        fields=['liked_post','post_details','date']

class OwnPostLikesSerializer(serializers.ModelSerializer):

    class Meta:
        model=Posts
        fields=[
            #'username',
            #'owner',
            'title',
            'post',
            #'date',
            ]
class OwnPostsSerializer(serializers.ModelSerializer):
    liked_by_details=UserDetailSerializer(source='get_user_details',many=True)
    post=OwnPostLikesSerializer(source='get_details',many=True)
    class Meta:
        model=Likes
        fields=['id','liked_post','post','liked_by','liked_by_details','date']

class CommentedSerializer(serializers.ModelSerializer):
    post_det=PostLikesSerializer(source='get_comm_det',many=True)
    class Meta:
        model=Comments
        fields=['id','post','comment','date','post_det']

class CommentsOnOwnPostsSerializer(serializers.ModelSerializer):
    commenter_details=UserDetailSerializer(source='get_user_det',many=True)
    pst_detail=OwnPostLikesSerializer(source='get_details',many=True)
    class Meta:
        model=Comments
        fields=['post','pst_detail','comment','commenter_id','commenter_name','commenter_details','date']
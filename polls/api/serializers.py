from rest_framework import serializers
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from polls.models import Posts,Onetimelinks
from django.db.models import Q

User=get_user_model()
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Posts
        fields=[
            'username',
            'title',
            'post',
            'date',
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
    email=email=serializers.EmailField(label='Email Address',required=True,allow_blank=False)
    class Meta:
        model=User
        fields=[
            'email'
            ]
    def validate(self,data):
        user_obj=None
        email=data.get("email",None)
        user=User.objects.filter(Q(email=email))
        if user.exists() and user.count()==1:
            for user in user:
                user= user
                t=ceil(time())
                Onetimelinks.objects.filter(code=user.pk).delete()
                u=Onetimelinks(code=user.pk,token=t)
                u.save()
                t=str(t).encode()
                subject='Reset link for password'
                message = render_to_string('polls/password_resetlink_generation.html', {
                    'user': user,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':urlsafe_base64_encode(force_bytes(t)),
                    })
                    
                from_mail=settings.EMAIL_HOST_USER
                to_mail=[email]
                send_mail(subject,message,from_mail,to_mail,fail_silently=False)
        else:
            raise serializers.ValidationError("Email is not registered or not valid")
        return data

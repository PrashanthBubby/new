from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from polls.models import Posts
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

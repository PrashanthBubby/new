from rest_framework.generics import (ListAPIView,
                                     CreateAPIView,
                                     UpdateAPIView,
                                     RetrieveAPIView,
                                     RetrieveUpdateAPIView,
                                     )
from polls.models import Posts,UserProfile
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
User=get_user_model()
from .serializers import (
    PostSerializer,
    UserLoginSerializer,
    EmailSerializer,
    ProfileSerializer,
    PostCreateSerializer
    )

class PostListAPIView(ListAPIView):
    queryset=Posts.objects.all().order_by('-date')
    serializer_class=PostSerializer

class PostCreateAPIView(CreateAPIView):
    queryset=Posts.objects.all()
    serializer_class=PostCreateSerializer
    

    def perform_create(self,serializer):
        t=datetime.datetime.now()
        serializer.save(username=self.request.user,date=t)

#class ProfileListAPIView(LoginRequiredMixin,ListAPIView):
 #   login_url= '/polls/login/'
#class ProfileListAPIView(ListAPIView):
    #queryset=UserProfile.objects.all()
    #serializer_class=ProfileSerializer
class ProfileListAPIView(ListAPIView):
    serializer_class=ProfileSerializer
    def get_queryset(self):
        user = self.request.user
        queryset=UserProfile.objects.filter(name=user)
        return queryset
class ProfileListAPIView(ListAPIView):
    serializer_class=ProfileSerializer
    def get_queryset(self):
        user = self.request.user
        queryset=UserProfile.objects.filter(name=user)
        return queryset

class ProfileUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class=ProfileSerializer
    def get_queryset(self):
        user = self.request.user
        queryset=UserProfile.objects.filter(name=user)
        return queryset


class ProfileEditAPIView(UpdateAPIView):
    serializer_class=ProfileSerializer
    def get_queryset(self):
        user = self.request.user
        
        queryset=UserProfile.objects.filter(name=user)
        return queryset
    def update(self,request,*args,**kwargs):
        instance = self.get_object()
        instance.school = request.data.get("school")
        user = self.request.user
        UserProfile.objects.filter(name=user).update(school='dishum',
                                                     college='somecollege',
                                                     highlight='some',
                                                     subjects='sub',
                                                     stream='stream',
                                                     projects='proj',
                                                     internship='intern',
                                                     phone=9874562589
                                                     )
        return Response('done')
        
class PostUpdateAPIView(ListAPIView):
    queryset=Posts.objects.all()
    serializer_class=PostSerializer



class UserLoginAPIView(APIView):
    permission_classes=[AllowAny]
    serializer_class=UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data=request.data
        serializer=UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data=serializer.data
            return Response(new_data,status=HTTP_200_OK)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)

class EmailSendingAPIView(APIView):
    permission_classes=[AllowAny]
    serializer_class=EmailSerializer

    def post(self, request, *args, **kwargs):
        data=request.data
        serializer=EmailSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data=serializer.data
            return Response(new_data,status=HTTP_200_OK)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)

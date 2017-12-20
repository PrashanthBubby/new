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
from django.http import HttpResponse
User=get_user_model()
from .serializers import (
    PostSerializer,
    UserLoginSerializer,
    EmailSerializer,
    ProfileSerializer,
    PostCreateSerializer,
    EmailInviteSerializer,
    OtherInviteSerializer,
    )
import json
class PostListAPIView(ListAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Posts.objects.all().order_by('-date')
    serializer_class=PostSerializer

class PostCreateAPIView(CreateAPIView):
    permission_classes=[IsAuthenticated]
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
    permission_classes=[IsAuthenticated]
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

#this is nit used from gere(
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
#up to here)


        
class PostUpdateAPIView(ListAPIView):
    permission_classes=[IsAuthenticated]
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

class EmailInviteAPIView(APIView):
    permission_classes=[IsAuthenticated]
    serializer_class=EmailInviteSerializer
    def post(self, request, *args, **kwargs):
        data=request.data
        context = {"request": self.request,}
        serializer=EmailInviteSerializer(data=data,context=context)
        if serializer.is_valid(raise_exception=True):
            new_data=serializer.data
            return Response('your invitation is on its way')
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)

"""
    def post(self,request):
        user=request.user
        data=request.data
        serializer=EmailSerializer(data=data)
        return Response({'username':user.email})
"""
class InviteOtherAPIView(APIView):
    permission_classes=[IsAuthenticated]
    serializer_class=EmailInviteSerializer
    def get(self,request,*args,**kwargs):
        data=request.data
        context = {"request": self.request,}
        serializer=OtherInviteSerializer(data=data,context=context)
        if serializer.is_valid(raise_exception=True):
            #new_data=serializer.data
            #userid=int(serializer.data['user'])
            user=self.request.user.username
            message='Your friend '+user+' wants you to join kriger campus on http://bit.do/kcapp' 
            ser=json.dumps({'invite':message}, sort_keys=True,indent=4, separators=(',', ': '))
            return HttpResponse(ser)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)
        

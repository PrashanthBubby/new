from rest_framework.generics import (ListAPIView,
 UpdateAPIView,
RetrieveUpdateAPIView,
)
from polls.models import Posts,UserProfile
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin

User=get_user_model()
from .serializers import (
    PostSerializer,
    UserLoginSerializer,
    EmailSerializer,
    ProfileSerializer
    )

class PostListAPIView(ListAPIView):
    queryset=Posts.objects.all()
    serializer_class=PostSerializer

#class ProfileListAPIView(LoginRequiredMixin,ListAPIView):
 #   login_url= '/polls/login/'
#class ProfileListAPIView(ListAPIView):
    #queryset=UserProfile.objects.all()
    #serializer_class=ProfileSerializer
class ProfileListAPIView(ListAPIView):
    serializer_class=ProfileSerializer
    def get(self, request):
        permission_classes=[IsAuthenticated]
        if request.user.is_authenticated():
            serializer = ProfileSerializer(request.user.userprofile)
            return Response(serializer.data)
        else: return Response('not logged in.please login to view your profile')

class ProfileEditAPIView(APIView):
    serializer_class=ProfileSerializer
    def get(self, request):
        permission_classes=[IsAuthenticated]
        if request.user.is_authenticated():
            serializer = ProfileSerializer(request.user.userprofile)
            return Response(serializer.data)
        else: return Response('not logged in.please login to view your profile')
    def post(self, request, *args, **kwargs):
        data=request.data
        serializer=ProfileSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data=serializer.data
            return Response(new_data,status=HTTP_200_OK)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)

        
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

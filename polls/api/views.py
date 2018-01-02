from rest_framework.generics import (ListAPIView,
                                     CreateAPIView,
                                     UpdateAPIView,
                                     RetrieveAPIView,
                                     RetrieveUpdateAPIView,
                                     )
from polls.models import Posts,UserProfile,Requests,Comments,Likes
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from django.http import HttpResponse
User=get_user_model()
from .serializers import (#importing serializers
    PostSerializer,
    UserLoginSerializer,
    EmailSerializer,
    ProfileSerializer,
    PostCreateSerializer,
    EmailInviteSerializer,
    OtherInviteSerializer,
    SendRequestsSerializer,
    RequestsSerializer,
    CommentsSerializer,
    CommentCreateSerializer,
	LikesSerializer,
    OwnPostsSerializer,
    CommentedSerializer,
    CommentsOnOwnPostsSerializer,
    LikedSerializer,
    )
import json
class PostListAPIView(ListAPIView):#returns list of all posts
    permission_classes=[IsAuthenticated]# permissions.allows only if the user is authenticated
    queryset=Posts.objects.all().order_by('-date')
    serializer_class=PostSerializer#using the imported serializer


class PostCreateAPIView(CreateAPIView):#create  the post
    permission_classes=[IsAuthenticated]
    queryset=Posts.objects.all()
    serializer_class=PostCreateSerializer
    

    def perform_create(self,serializer):
        t=datetime.datetime.now()#getting the present time
        serializer.save(username=self.request.user,date=t,name=self.request.user.username)#saving the instance of the post

class CommentCreateAPIView(CreateAPIView):#commenting on a post
    permission_classes=[IsAuthenticated]
    queryset=Comments.objects.all()
    serializer_class=CommentCreateSerializer

    def perform_create(self,serializer):
        t=datetime.datetime.now()
        serializer.save(commenter_id=self.request.user,commenter_name=self.request.user.username,date=t)
"""        
class LikesCreateAPIView(CreateAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Likes.objects.all()
    serializer_class=LikesSerializer
    def perform_create(self,serializer):
	    serializer.save(liked_by=self.request.user,liked_by_name=self.request.user.username)
"""
#class ProfileListAPIView(LoginRequiredMixin,ListAPIView):
 #   login_url= '/polls/login/'
#class ProfileListAPIView(ListAPIView):
    #queryset=UserProfile.objects.all()
    #serializer_class=ProfileSerializer

class ProfileListAPIView(ListAPIView):#To view the profile a authenticated user
    serializer_class=ProfileSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        queryset=UserProfile.objects.filter(name=user)#filtering to get the details of the requested user
        return queryset#returning the result

class ProfileUpdateAPIView(RetrieveUpdateAPIView):#udating the profile
    serializer_class=ProfileSerializer
    def get_queryset(self):
        user = self.request.user
        queryset=UserProfile.objects.filter(name=user)
        return queryset

#the below class is not used from (
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



class UserLoginAPIView(APIView):#checks the given details and returns wether the credentials are valid or invalid 
    permission_classes=[AllowAny]
    serializer_class=UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data=request.data#getting data from the form
        serializer=UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):#To check wether the data is valid or not
            new_data=serializer.data
            return Response(new_data,status=HTTP_200_OK)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)#returns error 400 if the data is invalid

class EmailSendingAPIView(APIView):#to send the email 
    permission_classes=[AllowAny]
    serializer_class=EmailSerializer

    def post(self, request, *args, **kwargs):
        data=request.data
        serializer=EmailSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data=serializer.data
            return Response(new_data,status=HTTP_200_OK)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)
 
class EmailInviteAPIView(APIView):#to invite through email
    permission_classes=[IsAuthenticated]
    serializer_class=EmailInviteSerializer
    def post(self, request, *args, **kwargs):
        data=request.data
        context = {"request": self.request,}#sending request through context
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
#not using this code
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
        

class RequestsListAPIView(ListAPIView):#returns all the requests that user had sent
    permission_classes=[IsAuthenticated]
    serializer_class=RequestsSerializer
    def get_queryset(self):
        user=self.request.user
        queryset=Requests.objects.all().filter(requested_by_id=user)
        return queryset
        
class SendRequestsAPIView(ListAPIView):#send requests
    permission_classes=[IsAuthenticated]    
    serializer_class=SendRequestsSerializer
    def get_queryset(self):
        user = self.request.user
        queryset=User.objects.all().exclude(username=user)
        return queryset

    def post(self,request,*args,**kwargs):
        user = self.request.user.id
        data=request.data
        user_to=int(data['username'])
        if(user_to==user):
            return Response('Error while sending request')
        else:
            x=User.objects.get(id=user)
            x1=x.username
            y=User.objects.get(id=user_to)
            y1=y.username
            pre_req=Requests.objects.all().filter(requested_by_id=x).filter(requested_to_id=y)
            if pre_req.exists():#checking wether the user had already sent the request 
                return Response('Request sent')
            else:
                Requests.objects.create(requested_by_id=x,By_name=x1,requested_to_id=y,to_name=y1)#if not sent send req
                return Response('Request sent')
"""
class LikesCreateAPIView(UpdateAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Likes.objects.all()
    serializer_class=LikesSerializer
    def perform_create(self,serializer):
	    serializer.save(liked_by=self.request.user,liked_by_name=self.request.user.username)
"""
class LikesCreateAPIView(ListAPIView):#to like a post
    permission_classes=[IsAuthenticated]
    queryset=Likes.objects.all()
    serializer_class=LikesSerializer

    def post(self,request,*args,**kwargs):
        data=request.data
        post=int(data['liked_post'])#getting the id of the post
        y=Posts.objects.get(id=post)
        user=self.request.user
        user_name=self.request.user.username
        pre_exists=Likes.objects.all().filter(liked_post=post).filter(liked_by=user)#checking wether the like exists
        if pre_exists.exists():
            return Response('already liked')
        else:
            t=datetime.datetime.now()
            Likes.objects.create(liked_by=user,liked_by_name=user_name,liked_post=y,date=t)
            return Response('Liked post '+str(y))

class LikesAPIView(ListAPIView):#likes on each post
	permission_classes=[IsAuthenticated]
	serializer_class=LikesSerializer
	queryset=Likes.objects.all()
	def post(self,request,*args,**kwargs):
		data=request.data
		user=self.request.user.id
		post=int(data['liked_post'])
		x=Likes.objects.all().filter(liked_post=post)#getting likes of a post
		count=x.count()#counting no of likes
		likedby_details=[]
		#main_dic={}
		#n=1
		for idd in x:
			y=(idd.liked_by.id)
			sub_dic={}
			sub_dic={'image':[user.userprofile.image.url for user in User.objects.all().filter(id=int(y))],
			'first_name':[user.userprofile.first_name for user in User.objects.all().filter(id=int(y))],
			'last_name':[user.userprofile.last_name for user in User.objects.all().filter(id=int(y))]
			}
			likedby_details.append(sub_dic.copy())
			#main_dic.update(sub_dic)
			#n=n+1
		return Response({"likes_count":count,"details":likedby_details})

        
class CommentsAPIView(ListAPIView):#to view all comments on a post
    permission_classes=[IsAuthenticated]
    serializer_class=CommentsSerializer
    queryset=Posts.objects.all()
"""
class LikesOnOwnPostAPIView(ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=OwnPostsSerializer
    def get_queryset(self,*args,**kwargs):
        user = self.request.user
        queryset=Posts.objects.all().filter(username=user).filter(id__)
        return queryset
"""
class LikesOnLikedPostAPIView(ListAPIView):#notifications.likes on liked post
    permission_classes=[IsAuthenticated]
    serializer_class=LikedSerializer
    def get_queryset(self,*args,**kwargs):
        user = self.request.user
        queryset=Likes.objects.all().filter(liked_by=user).order_by('-date')#filtering each post and arranging them by date
        return queryset

class CommentsOnCommentedPostAPIView(ListAPIView):#notifications.comments on commented post
    permission_classes=[IsAuthenticated]
    serializer_class=CommentedSerializer
    def get_queryset(self,*args,**kwargs):
        user = self.request.user
        queryset=Comments.objects.all().filter(commenter_id=user).order_by('-date')
        return queryset

class LikesOnOwnPostAPIView(ListAPIView):#likes on own post
    permission_classes=[IsAuthenticated]
    serializer_class=OwnPostsSerializer
    def get_queryset(self,*args,**kwargs):
        user = self.request.user
        posts=Posts.objects.all().filter(username=user)#posts of a requested user
        queryset=Likes.objects.all().filter(liked_post__id__in=[e.id for e in posts]).order_by('-date')#filtering and checking the likes on the post
        return queryset

class CommentsOnOwnPostAPIView(ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=CommentsOnOwnPostsSerializer
    def get_queryset(self,*args,**kwargs):
        user = self.request.user
        posts=Posts.objects.all().filter(username=user)#posts of a requested user
        queryset=Comments.objects.all().filter(post__id__in=[e.id for e in posts]).order_by('-date')#filtering and checking the comments on the post
        return queryset
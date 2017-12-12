from django.shortcuts import render , redirect
from django.template.loader import render_to_string
from django.shortcuts import HttpResponse
from polls.models import Posts,UserProfile,Onetimelinks
import datetime
from django.http import HttpResponseRedirect
from .forms import Posts_Details, User_Signup, Update_Profile, Mail_to,Reset
from django.views import generic
from django.contrib.auth.models import User
from django.urls import reverse

from django.conf import settings
from django.core.mail import send_mail

def signup(request):
    return render(request, 'polls/signup.html')

def signup_cr(request):
    if request.method=='POST':
        form=User_Signup(request.POST)
    if form.is_valid():
        user_nme=form.cleaned_data['username']
        pswrd=form.cleaned_data['password']
        email=form.cleaned_data['email']
        
        user = User.objects.create_user(user_nme,email,pswrd)
        return render(request,'polls/signup_done.html')
    else: return HttpResponse('enter correct format')
    

#def blog(request):
#   return render(request,'polls/blog.html')
def profile(request):
    return render(request,'polls/profile.html')

def edit_profile(request):
    return render(request,'polls/edit_profile.html')

def update_profile(request):
    if request.method=='POST':
        form=Update_Profile(request.POST)

        
        f_name=request.POST['firstname']
        l_name=request.POST['lastname']
        scl=request.POST['school']
        clg=request.POST['college']
        hl=request.POST['highlight']
        suj=request.POST['subjects']
        strm=request.POST['stream']
        proj=request.POST['projects']
        intern=request.POST['internship']
        phone=request.POST['phone']
        z=request.user.username
        u=User.objects.get(username=z)
        u.first_name=f_name
        u.last_name=l_name
        x=UserProfile.objects.get(name__username=z)
        x.school=scl
        x.college=clg
        x.highlight=hl
        x.subjects=suj
        x.stream=strm
        x.projects=proj
        x.internship=intern
        x.phone=phone
        u.save()
        x.save()
        return render(request,'polls/profile.html')
    else:return HttpResponse('form submission ok but something wrong with details')

    
def submit_post(request):
    if request.method=='POST':
        form=Posts_Details(request.POST)
    if form.is_valid():
        post_title=form.cleaned_data['title']
        post_matter=form.cleaned_data['post']
        t=datetime.datetime.now()
        data=Posts(username=request.user,title=post_title,post=post_matter,date=t)
        data.save()
        return redirect('posts')
    else: return HttpResponse('some thing went wrong')

def forgot_password(request):
    return render(request,'polls/forgot_password.html')



from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.db.models.query_utils import Q
from time import time
from math import ceil,floor

def verify_link(request,code,token):
    code=urlsafe_base64_decode(force_bytes(code))
    code=code.decode()
    code=int(code)
    token=urlsafe_base64_decode(force_bytes(token))
    token=token.decode()
    requested_time=int(token)
    present_time=int(ceil(time()))
    time_btwn=present_time-requested_time
    time_btwn=floor(time_btwn/60)
    if(time_btwn>=500):
        return HttpResponse(' 1 the link is expired or used')
    activelinks=Onetimelinks.objects.all().filter(Q(code=code)).filter(Q(token=token))
    if activelinks.exists():
        if request.method=='POST':
            form=Reset(request.POST)
            if form.is_valid():
                password=form.cleaned_data['password']
                u=User.objects.get(pk=code)
                old=u.password
                u.set_password(password)
                Onetimelinks.objects.filter(code=u.pk).delete()
                return HttpResponse('done')
            else:return HttpResponse('not valid form')
        else:
            activelinks=Onetimelinks.objects.all().filter(Q(code=code)).filter(Q(token=token))
            if activelinks.exists():
                for user in activelinks:
                    associated_user=User.objects.all().filter(Q(pk=code))
                    if associated_user.exists():
                        for user in associated_user:
                            email=user.email
                            c={'usermail':email}
                            return render(request,'polls/reset_password.html',c)
                    else:return HttpResponse('the link is expired or already used')
            else:return HttpResponse('2 the link is already used or expired')
    else:return HttpResponse('3 the link is already used or expired')
def verification_code_to_mail(request):
    if request.method=='POST':
        form=Mail_to(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email_to']
            associated_users= User.objects.filter(Q(email=email))
            if associated_users.exists():
                for user in associated_users:
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
                return HttpResponse('Reset link has bees sent to the registered mail id.Please follow the link to reset password')
            else:return HttpResponse('not registered')
        else:return HttpResponse('form not valid')
    else:return HttpResponse('some thing went wrong')

def blog(request):
    return render(request,'polls/blog.html')

def createpost(request):
    return render(request,'polls/post_entry.html')

#def submit_post(request):
 #   return render(request,'polls/posts_lists.html') 

def followers(request):
    return render(request, 'polls/signin_error.html')


class Postssss(generic.ListView):
    template_name='polls/posts_lists.html'
    def get_queryset(self):
        return Posts.objects.all().order_by('-date')
class DPostssss(generic.DetailView):
    model=Posts
    template_name='polls/detail_post.html'



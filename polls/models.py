from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    image=models.ImageField(upload_to='profile_pic',blank=True,default='profile')
    first_name=models.CharField(max_length=100,null=True,blank=True)
    last_name=models.CharField(max_length=100,null=True,blank=True)
    name=models.OneToOneField(User,on_delete=models.CASCADE)
    school=models.CharField(max_length=100,null=True,blank=True)
    college=models.CharField(max_length=150,null=True,blank=True)
    highlight=models.CharField(max_length=150,null=True,blank=True)
    subjects=models.CharField(max_length=150,null=True,blank=True)
    stream=models.CharField(max_length=150,null=True,blank=True)
    projects=models.CharField(max_length=150,null=True,blank=True)
    internship=models.CharField(max_length=150,null=True,blank=True)
    hobbies=models.CharField(max_length=150,null=True,blank=True)
    phone=models.BigIntegerField(null=True,blank=True)

    def __str__(self):
        return self.name.username

class Posts(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=150,default='name')
    title=models.TextField(max_length=150)
    post=models.TextField()
    date=models.DateTimeField(default='')

    def __str__(self):
        return self.title

    def get_user_details(self):
        return UserProfile.objects.filter(name__posts=self)

    def get_post_comments(self):
        posts=Posts.objects.all()
        return Comments.objects.all().filter(post__id=self.id)
    def get_likes(self):
        return Likes.objects.all().filter(liked_post__id=self.id)
    def get_owner(self):
        return UserProfile.objects.filter(name=self.username)
from django.db.models.signals import post_save
def create_profile(sender,**kwargs):
    if kwargs['created']:
        user_profile=UserProfile.objects.create(name=kwargs['instance'])
post_save.connect(create_profile,sender=User)

class Onetimelinks(models.Model):
    code=models.CharField(max_length=100,null=False,blank=False)
    token=models.CharField(max_length=100,null=False,blank=False)

    def __str__(self):
        return self.token
class Comments(models.Model):
    post=models.ForeignKey(Posts,on_delete=models.CASCADE)
    comment=models.CharField(max_length=500,null=True,blank=True)
    commenter_id=models.ForeignKey(User,on_delete=models.CASCADE)
    commenter_name=models.CharField(max_length=150,default='name')
    date=models.DateTimeField(default='1999-01-01 01:01:01')
    def __str__(self):
        return self.comment
    def get_user_details(self):
        return UserProfile.objects.filter(name__comments=self.id)
    def get_comm_det(self):
        return Posts.objects.all().filter(title=self.post)
    def get_details(self):
        return Posts.objects.all().filter(title=self.post)
    def get_user_det(self):
        return UserProfile.objects.all().filter(name=self.commenter_id)

class Requests(models.Model):
    requested_by_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='request_created')
    By_name=models.CharField(max_length=150,null=False,default='user')
    requested_to_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='request_received')
    to_name=models.CharField(max_length=150,null=False,default='user')



class Likes(models.Model):
    liked_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name='liked_by')
    liked_by_name=models.CharField(max_length=150,null=False,default='user')
    liked_post=models.ForeignKey(Posts,on_delete=models.CASCADE,related_name='liked_pooost')
    date=models.DateTimeField(default='1999-01-01 01:01:01')

    def __str__(self):
        return self.liked_by_name+' liked '+str(self.liked_post)
    def get_details(self):
        return Posts.objects.all().filter(title=self.liked_post)
    def get_user_details(self):
        return UserProfile.objects.all().filter(name=self.liked_by)

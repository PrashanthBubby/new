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
    title=models.TextField(max_length=15)
    post=models.TextField()
    date=models.DateTimeField(default='')

    def __str__(self):
        return self.title
    
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

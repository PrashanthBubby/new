from django import forms


class Posts_Details(forms.Form):
    title=forms.CharField(label='title',max_length=200)
    post=forms.CharField(label='post',max_length=500)
class User_Signup(forms.Form):
    username=forms.CharField(label='username',max_length=200)
    password=forms.CharField(label='passwoed',max_length=500)
    email=forms.CharField(label='email',max_length=200)
class Update_Profile(forms.Form):
    firstname=forms.CharField(label='firstname',max_length=200)
    lastname=forms.CharField(label='lastname',max_length=200)
    school=forms.CharField(label='school',max_length=200)
    college=forms.CharField(label='college',max_length=200)
    highlight=forms.CharField(label='highlight',max_length=200)
    subjects=forms.CharField(label='subjects',max_length=200)
    stream=forms.CharField(label='stream',max_length=200)
    projects=forms.CharField(label='projects',max_length=200)
    internship=forms.CharField(label='internship',max_length=200)    
    phone=forms.IntegerField(label='phone')

class Mail_to(forms.Form):
    email_to=forms.CharField(label='email_to',max_length=200)
class Reset(forms.Form):
    password=forms.CharField(label='pass',max_length=50)

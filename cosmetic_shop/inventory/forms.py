from .models import products,inventordetails
from django import forms
from django.contrib.auth.models import User
from django. contrib.auth.forms import UserCreationForm

class createuser(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password1','password2','email']


class creatproduct(forms.ModelForm):
    class Meta:
        model=products
        fields='__all__'

class createinventor(forms.ModelForm):
    class Meta:
        model=inventordetails
        fields='__all__'
 

from django import forms
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm

from .models import UserProfile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(widget=forms.TextInput() ,required=True)
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required= True)
    # mobile_Num = forms.NumberInput()

    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'password1',
                  'password2',
                  )

        def save(self, commit=True):
            user = super(RegistrationForm, self).save(commit=False)
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.username = self.cleaned_data['username']
            user.password1 = self.cleaned_data['password1']
            user.password2 = self.cleaned_data['password2']
            # user.mobile_Num = self.cleaned_data['mobile_Num']

            if(commit):
                user.save()
            return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('address','mobile')

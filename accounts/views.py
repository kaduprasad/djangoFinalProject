from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import RegistrationForm
from django.contrib.auth import login, logout, authenticate
from .forms import *

from django import forms


# Create your views here.

def signup_view(request):
    if request.method == 'POST':

        form = RegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            user =  form.save() # log user in
            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()
            mobile  = form.cleaned_data.get('mobile')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username= username or mobile,password = password)

            login(request, user)
            return redirect('BrainTumorDetection')

    else:
        form = RegistrationForm()
        profile_form = UserProfileForm()
    context = {'form': form, 'profile_form':profile_form}
    return render(request, 'accounts/signup.html',context) #{'form': form})


def login_view(request):
    if request.method == 'POST':

        form = AuthenticationForm(data=request.POST)
        # form = RegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        USERNAME_FIELD = 'mobile'

        if form.is_valid():
            user = form.get_user()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)

            login(request, user)
            return redirect('articles:list')
            # login(request, user)
            # return redirect('articles:list') # login user
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})



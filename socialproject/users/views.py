from django.shortcuts import render, redirect
from .forms import LoginForm, UserRegisterForm, ProfileEditForm, UserEditForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile
from posts.models import Posts



def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username = data['username'], password = data['password'])
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return HttpResponse('Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('index')


@login_required
def index(request):
    current_user = request.user
    posts = Posts.objects.filter(user=current_user)
    profile = Profile.objects.filter(user=current_user).first()
    return render(request, 'index/index.html', {'posts': posts, 'profile': profile})


def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'users/register_done.html')
    else:
        user_form = UserRegisterForm()
    return render(request, 'users/register.html', {'user_form': user_form})


@login_required
def edit(request):
    try:
        profile_instance = request.user.profile
    except Profile.DoesNotExist:
        profile_instance = None
    
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=profile_instance, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            if profile_instance:
                profile_form.save()
            else:
                profile = profile_form.save(commit=False)
                profile.user = request.user
                profile.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=profile_instance)
    return render(request, 'users/edit.html', {'user_form': user_form, 'profile_form': profile_form})


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import SigninForm


def index(request):
    return render(request, 'index.html')


def signin(request):
    if request.user.is_authenticated:
        return redirect(reverse('profile'))
    err_msg = None
    if request.method == 'POST':
        form = SigninForm(request.POST)
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        userlogin = authenticate(username=username, password=password)
        if userlogin is not None:
            login(request, userlogin)
            request.session['username'] = username
            return redirect(reverse('profile'))
        else:
            err_msg = 'Email or password incorrect'
    else:
        form = SigninForm()
    return render(request, 'signin.html', {'form': form, 'err_msg': err_msg})


@login_required(login_url='signin')
def signout(request):
    logout(request)
    return redirect(reverse('index'))


@login_required(login_url='signin')
def profile(request):
    #    if request.user.is_authenticated:
    #        username = request.user
    #        return render(request, 'profile.html', {'username': username})
    #    else:
    #        return redirect(reverse('signin'))
    username = request.user
    return render(request, 'profile.html', {'username': username})

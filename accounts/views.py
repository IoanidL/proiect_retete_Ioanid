from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

def registration_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(request.GET.get('next', '/'))

    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})



def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(request.GET.get('next', '/'))
        else:
            return redirect('login_error')

    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def login_error(request):
    return render(request, 'accounts/login_error.html')


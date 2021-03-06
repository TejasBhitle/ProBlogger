from django.contrib.auth import (authenticate,
get_user_model,
login,
logout)

from django.shortcuts import render, redirect
from .user_form import UserLoginForm, UserRegisterForm


# Create your views here.
def login_view(request):
    form = UserLoginForm(request.POST or None)
    next_var = request.GET.get('next')
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        if next_var:
            return redirect(next_var)
        return redirect("/posts/")

    context = {
        "form": form,
        "title": "Login",
    }
    return render(request, "user_form.html", context)


def register_view(request):
    form = UserRegisterForm(request.POST or None)
    next_var = request.GET.get('next')
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next_var:
            return redirect(next_var)
        return redirect("/posts/")

    context = {
        "form": form,
        "title": "Register"
    }
    return render(request, "user_form.html", context)

'''
def auth_view(request):
    form1 = UserLoginForm(request.POST or None)
    form2 = UserRegisterForm(request.POST or None)
    context = {
        "form1": form1,
        "form2": form2,
        "title": "Auth View",
    }
    return render(request, "index.html", context)
'''


def logout_view(request):
    logout(request)
    return redirect("/")

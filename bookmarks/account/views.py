from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from django.contrib.auth import authenticate, login
from django.shortcuts import render

from account.forms import LoginForm


# 로그인
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request=request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Authentication successfully")
                else:
                    return HttpResponse("Disabled account")
        else:
            return HttpResponse("Invalid login")
    else:
        form = LoginForm()
    return render(request, 'account/login.html',{'form':form})


@login_required
def dashboard(request):
    return render(request,
                  "account/dashboard.html",
                  {'section':'dashboard'})


from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

def index(request):
    if 'user_id' in request.session:
        return redirect('/travels')
    else:
        return render(request, 'login_app/index.html')

def register(request):
    result = User.objects.register(request.POST)
    if result[0] == True:
        request.session['user_id'] = result[1].id
        messages.success(request, "Registered!")
        return redirect('/travels')
    else:
        for error in result[1]:
            messages.error(request, error)
        return redirect('/')

def login(request):
    result = User.objects.login(request.POST)
    if result[0] == True:
        request.session['user_id'] = result[1].id
        return redirect('/travels')
    else:
        for error in result[1]:
            messages.error(request, error)
        return redirect('/')

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        messages.success(request, "logged out")
        return redirect('/')

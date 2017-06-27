from django.shortcuts import render, redirect
from ..login_app.models import User
from .models import Trip
from django.contrib import messages

def index(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'all_user': user,
            'trips': Trip.objects.all().filter(group=user),
            'users': Trip.objects.all().exclude(group=user)
        }
        return render(request, 'travel_app/index.html', context)
    else:
        return redirect('/')

def add(request):
    return render(request, 'travel_app/add.html')

def process(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['user_id'])
        result = Trip.objects.addTrip(request.POST, user)
        if result[0] == True:
            messages.success(request, result[1])
            return redirect('/travels')
        else:
            for error in result[1]:
                messages.error(request, error)
            return redirect('/add')

def destination(request, trip_id):
    context = {
        'trips': Trip.objects.get(id=trip_id),
        'group': User.objects.filter(trips__id=trip_id)
    }
    return render(request,'travel_app/destination.html', context)

def join(request, trip_id):
    user = User.objects.get(id=request.session['user_id'])
    result = Trip.objects.joinTrip(trip_id, user)
    messages.success(request, result[1])
    return redirect('/travels')

def logout(request):
    request.session.clear()
    return redirect('/')

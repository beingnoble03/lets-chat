from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.http import JsonResponse
import json
import datetime
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
# Create your views here.

def indexView(request):
    if not request.user.is_authenticated:
        return redirect(registerView)
    return render(request, 'index.html')

def loginView(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect(indexView)
        else:
            context['failed'] = True
    return render(request, 'login.html', context=context)

def registerView(request):
    context = {}
    if request.method == "POST":
        try:
            username = request.POST['username']
            password = request.POST['password']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            user = User.objects.create_user(username=username, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            login(request, user)
            return redirect(indexView)
        except:
            context['failed'] = True

    return render(request, 'register.html', context=context)

def logoutView(request):
    logout(request)
    return redirect(loginView)

@csrf_exempt
def sendMessage(request):
    response_data = {}
    if request.method == 'POST':
        request_json = json.loads(request.body.decode("utf-8").replace("'",'"'))
        username = request_json['username']
        message = request_json['message']
        user = User.objects.get(username=username)
        Message.objects.create(username=username, message=message, first_name=user.first_name, last_name=user.last_name, date=datetime.date.today(), time=datetime.datetime.now())
        response_data = {'success': True}
    return JsonResponse(response_data)

@csrf_exempt
def getMessages(request):
    all_messages = Message.objects.all()
    response_data = {'messages': []}
    for each_message in all_messages:
        message = {}
        message['message'] = each_message.message
        message['username'] = each_message.username
        message['date'] = each_message.date.strftime("%d/%m/%Y")
        message['time'] = each_message.time.strftime("%H:%M:%S")
        message['first_name'] = each_message.first_name
        message['last_name'] = each_message.last_name
        response_data['messages'].append(message)
    return JsonResponse(response_data)
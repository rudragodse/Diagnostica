from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
# Create your views here.
def userauth(request):

    if 'loginbtn' in request.POST:
        username = request.POST.get('username') #to get data from buttons;
        password = request.POST.get('pass')

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            messages.success(request,'Login Successful')
            

        if user is None:
            messages.error(request,'Login Unsuccessful')
    
    elif 'signupbtn' in request.POST:
        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        username=request.POST.get('username')
        emailid=request.POST.get('email')
        password=request.POST.get('signuppass')
        print(first_name,last_name,emailid,password)
        if User.objects.filter(username=username).exists():
            messages.error(request,'username already taken')
        elif User.objects.filter(email=emailid).exists():
            print('Email is already Taken')
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=emailid,
                first_name=first_name,
                last_name=last_name
            )
            user.save() 
    return render(request,'index.html')
    

def renderDisease(request):
    return render(request,'disease.html')

def renderSymptoms(request):
    return render(request,'symptoms.html')
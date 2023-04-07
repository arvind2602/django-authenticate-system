from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout

# Create your views here.
def home(request):
    return render(request,'index.html')
def handlesignup(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        cpassword=request.POST['cpassword']

        if password!=cpassword:
            messages.warning(request,"Password doesnot match")
            return render(request,'signup.html')
        try:
            if User.objects.get(username=username):
                messages.warning(request,"Username already used")
        except :
            pass

        myuser=User.objects.create_user(username,email,password)
        myuser.save()
        messages.info(request,"You have scussefully registered")
        return redirect('/login/')
            

    return render(request,'signup.html')
def handlelogin(request):

    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        myuser=authenticate(username=username,password=password)
        if myuser is not None :
            messages.info(request,"Logged in successfully")
            return redirect('/')
        else:
            messages.error(request,"User not found")
            return render('/login/')

    return render(request,'login.html')

def handlelogout(request):
    logout(request)
    messages.success(request,"Logout Success")
    return redirect('/login/')
    

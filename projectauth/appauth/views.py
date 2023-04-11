import django
from django.utils.encoding import force_str
django.utils.encoding.force_text = force_str
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from django.views.generic import View

# For activate account

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.urls import NoReverseMatch,reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError

# For sending email
from django.core.mail import send_mail,EmailMultiAlternatives
from django.core.mail import BadHeaderError,send_mail 
from django.core.mail import EmailMessage
from django.core import mail
from django.conf import settings

# Getting token from utils
from .utils import generate_token,TokenGenerator

# Reset Password Generaters
from django.contrib.auth.tokens import PasswordResetTokenGenerator


#threading
import threading

class EmailThread(threading.Thread):
    def __init__(self,email_message):
        self.email_message=email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()

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
                return redirect('/signup/')
        except :
            pass

        user=User.objects.create_user(username,email,password)
        user.is_active=False
        user.save()
        current_site=get_current_site(request)
        email_subject="Activate your account"
        message=render_to_string('activate.html',{
            'user':user,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)

        })
        email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)

        EmailThread(email_message).start()
        messages.info(request,"Activate your account from email",)
        return redirect('/login/')
            

    return render(request,'signup.html')

class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)

        except Exception as identifier:
            user=None
        
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.info(request,"Email Verified")
            return redirect('/login/')
        return render(request,'activatefail.html')






def handlelogin(request):

    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        myuser=authenticate(username=username,password=password)
        if myuser is not None :
            login(request,myuser)
            messages.info(request,"Logged in successfully")
            return redirect('/')
        else:
            messages.error(request,"User not found")
            return render('/login/')

    return render(request,'login.html')




# For Logout 

def handlelogout(request):
    logout(request)
    messages.success(request,"Logout Success")
    return redirect('/login/')


# for resetting password 

class RequestResetEmailView(View):
    def get(self,request):
        return render(request,"request-reset-email.html")
    
    def post(self,request):
        email=request.POST['email']
        user=User.objects.filter(email=email)

        if user.exists():
            current_site=get_current_site(request)
            email_subject='[Reset Your Password]'
            message=render_to_string('/reset-user-password.html',{
                'domain':current_site.domain,
                'UID':urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token':PasswordResetTokenGenerator.make_token(user[0])
            })

            email_message=EmailMessage(email_subject,message,settings.EMAIL_USER_HOST,[email])
            EmailThread(email_message).start()
            messages.info(request,"Email  for password reset is been sent")
            return render(request,'/request-reset-email.html')
        
class SetNewPasswordView(View):
    def get(self,request,uidb64,token):
        context={
            'uid':uidb64,
            'token':token,
        }
        try:
            user_id=force_text(urlsafe_base64_decode)
            user=User.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                messages.warning(request,"Password Rest Link is Invalid")
                return render(request,'/request-reset-password.html')
        
        except DjangoUnicodeDecodeError as identifier:
            pass

        return render(request,'/set-new-password.html')
    
    def post(self,request,uidb64,token):
        context={
            'uid':uidb64,
            'token':token,
        } 
        password=request.POST['password']
        cpassword=request.POST['cpassword']

        if password!=cpassword:
            messages.warning(request,"Password doesnot match")
            return render(request,'/set-new-password.html',context)
        
        try:
            user_id=force_text(urlsafe_base64_decode)
            user=User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request,"Password reset succesfully")
            return redirect(request,'/login/')

        except DjangoUnicodeDecodeError as identifier:
            messages.error(request,"Something went wrong")
            return redirect(request,'/set-new-password.html',context )


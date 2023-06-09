"""projectauth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.urls import path
from .views import handlesignup,home,handlelogin,handlelogout,ActivateAccountView,RequestResetEmailView,SetNewPasswordView


urlpatterns = [
   path('',home),
   path('signup/',handlesignup),
   path('login/',handlelogin),
   path('logout/',handlelogout),
   path('activate/<uidb64>/ <token>',ActivateAccountView.as_view(),name='activate'),
   path('request-reset-email/',RequestResetEmailView.as_view(),name="request-reset-email"),
   path('set-new-password/<uid64>/<token>',SetNewPasswordView.as_view(),name="set-new-password"),

]

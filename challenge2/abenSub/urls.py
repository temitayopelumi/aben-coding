"""abenSub URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views 
from django_registration.backends.one_step.views import RegistrationView
from django_registration.forms import RegistrationForm
from subscriptions.models import User
class MyCustomUserForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/register/',
        RegistrationView.as_view(
            form_class=MyCustomUserForm
        ),
        name='register',
    ),

    path('auth/accounts/',include('django_registration.backends.one_step.urls')),
    path('', include('subscriptions.urls')),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]

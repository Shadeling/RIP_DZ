"""mysite_1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from polls.views import *
from django.views.generic import ListView, DetailView
from polls.models import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin', admin.site.urls),
    path('addform', Add.as_view()),
    path('register', RegisterFormView.as_view(), name='reg'),
    path('login', LoginFormView.as_view(), name='login'),
    path('lul', LogoutView.as_view(), name='exit'),
    path('create', create),
    path('profile', update_profile, name='profile'),
    path('user/<int:id>', start, name='user'),
    path('', GamesList.as_view(), name='games_all'),
    path('games/<int:id>', GameView.as_view(), name='game'),

    url('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
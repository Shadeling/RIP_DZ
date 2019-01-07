from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from polls.models import *
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db import transaction
from polls.forms import *
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.views.generic.base import View
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages
from polls.serializers import *
from rest_framework import generics

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")

class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = "/"

    def form_valid(self, form):
        User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)

class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/profile/"
    template_name = "register.html"
    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)



class GameView(TemplateView):
    def get(self, *args, **kwargs):
        data = {
            'games': Games.objects.filter(id=kwargs['id']).first()
        }
        return render(self.request, 'address.html', data)

class GamesList(ListView):
    model=Games
    template_name='games.html'
    paginate_by=3
    queryset=Games.objects.all().order_by("-date")

def start(request):
    return 0

class Add(TemplateView):
    def get(self, request):
        return render(request, 'addform.html')

class Profile_View(TemplateView):
    def get(self, request):
        return render(request, 'profile.html')

def create(request):
    if request.method == "POST":
            tom = Games()
            tom.name = request.POST.get("name")
            tom.platform = request.POST.get("platform")
            tom.date = request.POST.get("date")
            tom.genre = request.POST.get("genre")
            tom.rating = request.POST.get("rating")
            tom.image = request.FILES['image']
            tom.info = request.POST.get("info")
            tom.save()
            return HttpResponseRedirect("/")
    return HttpResponseRedirect("addform")

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST,request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            '''messages.success(request, ('Your profile was successfully updated!'))'''
            return HttpResponseRedirect('profile')
        else:
            '''messages.error(request, ('Please correct the error below.'))'''
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


class GamesAPIView(generics.ListAPIView):
    queryset = Games.objects.all()
    model = Games
    serializer_class = GamesSerializer

class GameAPIView(generics.RetrieveAPIView):
    def get(self, *args, **kwargs):
        self.queryset=Games.objects.filter(id=kwargs['pk']).first()
        return super(GameAPIView, self).get(self)
    model = Games
    serializer_class = GamesSerializer
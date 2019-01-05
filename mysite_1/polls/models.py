from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from django.conf import settings

# Create your models here.
'''class BaseModel(models.Model):

    class Meta:
        abstract = True  # specify this model as an Abstract Model
        app_label = 'wdland'
'''

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    age= models.IntegerField(blank=True, null=True)
    image=models.ImageField(null=True, default = os.path.join('media/img/extra.png'), upload_to="img/users")
    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class Games(models.Model):
    name=models.CharField(max_length=100)
    platform=models.CharField(max_length=100)
    date=models.DateField()
    genre=models.CharField(max_length=100)
    rating=models.IntegerField()
    image=models.ImageField(upload_to="img/")
    info=models.TextField(default="")

    def __str__(self):
        return self.name
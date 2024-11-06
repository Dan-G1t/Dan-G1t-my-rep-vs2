from django.db import models
from django.contrib.auth.models import AbstractUser
from app_mountain_pass.resources import STATUS_TYPES, new


class CustomUser(AbstractUser):
    email = models.EmailField(unique = True)
    fam = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100)
    otc = models.CharField(max_length = 100)
    phone = models.CharField(unique = True, max_length = 15)


class Coordinates(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.FloatField()


class Level(models.Model):
    winter = models.CharField(max_length = 100, blank = True)
    summer = models.CharField(max_length = 100, blank = True)
    autumn = models.CharField(max_length = 100, blank = True)
    spring = models.CharField(max_length = 100, blank = True)


class Pass(models.Model):
    beauty_title = models.CharField(max_length = 255)
    title = models.CharField(max_length = 255)
    other_titles = models.TextField(blank = True)
    connect = models.TextField(blank = True)
    add_time = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    coords = models.ForeignKey(Coordinates, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

    status = models.CharField(max_length = 1, choices = STATUS_TYPES, default = new)

    def __str__(self):
        return self.title


class Image(models.Model):
    data = models.ImageField(upload_to='photos')
    title = models.CharField(max_length=255)
    pass_reference = models.ForeignKey(Pass, on_delete=models.CASCADE)


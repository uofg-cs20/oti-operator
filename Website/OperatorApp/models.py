from django.contrib.auth.models import User
from django.db import models


class Operator(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    modes = models.ManyToManyField('Mode')
    homepage = models.URLField()
    api_url = models.URLField()
    default_language = models.CharField(default='English', max_length=40)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    active = models.BooleanField(default=True)


    def __str__(self):
        return self.name



class Mode(models.Model):
    short_desc = models.CharField(max_length=50)
    long_desc = models.CharField(max_length=8000, null=True)

    def __str__(self):
        return self.short_desc

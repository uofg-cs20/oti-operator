from django.db import models

class Operator(models.Model):
    name = models.CharField(max_length=200)
    modes = models.ManyToManyField('Mode')
    
    homepage = models.URLField()
    api_url = models.URLField()
    default_language = models.CharField(max_length=40)
    phone = models.IntegerField(max_length=20)
    email = models.EmailField()
    active = models.BooleanField()


    def __str__(self):
        return self.name



class Mode(models.Model):
    short_desc = models.CharField(max_length=50)
    long_desc = models.CharField(max_length=8000)

    def __str__(self):
        return self.short_desc
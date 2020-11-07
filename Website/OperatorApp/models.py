from django.db import models

class Operator(models.Model):
    name = models.CharField(max_length=200)
    modes = models.ManyToManyField('Mode')

    def __str__(self):
        return self.name



class Mode(models.Model):
    short_desc = models.CharField(max_length=50)
    long_desc = models.CharField(max_length=8000)

    def __str__(self):
        return self.short_desc

from django.db import models

class Opinion(models.Model):
    firstname = models.CharField(max_length=128)
    lastname = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    opinion = models.TextField(max_length=1024)
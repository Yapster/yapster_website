from django.db import models

class Yap(models.Model):
    name = models.CharField(max_length=64)


class Library(models.Model):
    name = models.CharField(max_length=64)


class Profile(models.Model):
    name = models.CharField(max_length=64)
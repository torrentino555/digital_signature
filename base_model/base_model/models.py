# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Person(models.Model):
    user = models.OneToOneField(User)
    Surname = models.CharField(max_length=50)
    Firstname = models.CharField(max_length=50)
    GivenName = models.CharField(max_length=50)
    Country = models.CharField(max_length=50)
    State = models.CharField(max_length=50)
    Locality = models.CharField(max_length=50)
    StreetAddress = models.CharField(max_length=255)
    email = models.EmailField(max_length=50)
    INN = models.CharField(max_length=12)
    SNILS = models.CharField(max_length=11)
    admin = models.BooleanField(default=False);

    def __str__(self):
        return u'{} {} {}'.format(self.Surname, self.Firstname, self.GivenName)

class Order(models.Model):
    person = models.ForeignKey(Person)
    Isp = models.BooleanField()
    Token = models.BooleanField()
    Help = models.BooleanField()
    Date = models.DateField()
    Status = models.CharField(default=u'В рассмотрении', max_length=30)
    Number = models.IntegerField(default=0)
    Text = models.TextField(default='', max_length=500)

    def __str__(self):
        return u'{} {}'.format(self.person, self.Date)

class Meeting(models.Model):
    order = models.OneToOneField(Order)
    date = models.DateField()
    time = models.TimeField()

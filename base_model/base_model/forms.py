# -*- coding: utf-8 -*-
import datetime
from django import forms
from .models import Person, Order, Meeting
from django.contrib import auth
from django.contrib.auth.models import User
from .parser import xml_file, statement, invoice, in_pdf

class UserForm(forms.Form):
    Surname = forms.CharField(label=u'Имя')
    Firstname = forms.CharField(label=u'Фамилия')
    GivenName = forms.CharField(label=u'Отчество')
    Country = forms.CharField(label=u'Страна',widget=forms.TextInput(attrs={'value': 'RU'}))
    State = forms.CharField(label=u'Область', widget=forms.TextInput(attrs={'value': u"77 г. Москва"}))
    Locality = forms.CharField(label=u'Населенный пункт', widget=forms.TextInput(attrs={'value': u'г. Москва'}))
    StreetAddress = forms.CharField(label=u'Адрес')
    email = forms.EmailField()
    INN = forms.CharField(label=u'ИНН')
    SNILS = forms.CharField(label=u'СНИЛС')

    def save(self, user):
        f = Person.objects.get(user=user)
        f.Surname = self.cleaned_data['Surname']
        f.Firstname = self.cleaned_data['Firstname']
        f.GivenName = self.cleaned_data['GivenName']
        f.Country = self.cleaned_data['Country']
        f.State = self.cleaned_data['State']
        f.Locality = self.cleaned_data['Locality']
        f.StreetAddress = self.cleaned_data['StreetAddress']
        f.email = self.cleaned_data['email']
        f.INN = self.cleaned_data['INN']
        f.SNILS = self.cleaned_data['SNILS']
        f.save()

class LoginForm(forms.Form):
    login = forms.CharField(label=u'Логин')
    password = forms.CharField(label=u'Пароль', widget=forms.PasswordInput())
    __user = None

    def clean_password(self):
        try:
            self.__user = auth.authenticate(username=self.cleaned_data['login'], password=self.cleaned_data['password'])
            if self.__user is None:
                raise forms.ValidationError('')
        except:
            raise forms.ValidationError('Invaild login or password')

    def auth(self):
        return self.__user

class RegistrationForm(forms.Form):
    login = forms.CharField(label=u'Логин', max_length=50)
    password = forms.CharField(label=u'Пароль', widget=forms.PasswordInput(), min_length=5)
    password2 = forms.CharField(label=u'Повторите пароль', widget=forms.PasswordInput(), min_length=5)

    def clean_login(self):
        if User.objects.filter(username=self.cleaned_data['login']).count():
            raise forms.ValidationError(u'К сожалению этот логин уже занят')
        return self.cleaned_data['login']


    def clean_password2(self):
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise forms.ValidationError(u'Несовпадение введенных паролей')
        return self.cleaned_data['password2']

    def save(self):
        user = User.objects.create_user(username=self.cleaned_data['login'], password=self.cleaned_data['password'])
        user.save()
        person = Person(user=user)
        person.save()
        auth.authenticate(username=user.username, password=user.password)
        return user;

class OrderForm(forms.Form):
    Isp = forms.BooleanField(label='ISP', required=False)
    Token = forms.BooleanField(label='Token', required=False)
    Help = forms.BooleanField(label='Help', required=False)

    def save(self, person):
        order = Order(person=person)
        order.Isp = self.cleaned_data['Isp']
        order.Token = self.cleaned_data['Token']
        order.Help = self.cleaned_data['Help']
        order.Date = datetime.datetime.now()
        order.save()
        order.Number = order.id
        order.save()
        xml_file(person, order.pk)
        statement(person, order.pk)
        in_pdf('/home/olof/Projects/digital_signature/base_model/uploads/statements/' + str(order.pk) + '.xlsx', '/home/olof/Projects/digital_signature/base_model/uploads/statements/' + str(order.pk) + '.pdf')
        invoice(person, order.pk, order.Date)
        in_pdf('/home/olof/Projects/digital_signature/base_model/uploads/invoices/' + str(order.pk) + '.xlsx', '/home/olof/Projects/digital_signature/base_model/uploads/invoices/' + str(order.pk) + '.pdf')

class MeetingForm(forms.Form):
    Date = forms.DateField(label=u'Дата')
    Time = forms.TimeField(label=u'Время')

    def save(self, id):
        meeting = Meeting(order=Order.objects.get(pk=id))
        meeting.date = self.cleaned_data['Date']
        meeting.time = self.cleaned_data['Time']
        meeting.save()

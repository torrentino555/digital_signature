# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from .forms import UserForm, LoginForm, RegistrationForm, OrderForm,  MeetingForm
from django.contrib.auth.decorators import login_required
from .models import Person, Order, Meeting

def init(request, title, *args):
    context = {}
    context['title'] = title
    if request.user.is_authenticated:
        if len(args) != 0:
            context['menu'] = {args[0]: True}
        context['user'] = Person.objects.get(user=request.user)
    return context

@login_required(redirect_field_name='', login_url='/login/')
def order(request, number):
    content = init(request, u'Страница заказа')
    order = Order.objects.get(id=number)
    if request.method == 'POST':
        if request.POST['status'] == u'Принять':
            order.Status = u'Принято'
        else:
            order.Status = u'Отклонено'
        order.save()
        return HttpResponseRedirect(reverse('meeting', args=[number]))
    else:
        content['order'] = order
    if order.Status != 'В рассмотрении':
        content['meeting'] = Meeting.objects.get(order=content['order'])
    return render(request, 'order.html', content)

@login_required(redirect_field_name='', login_url='/login/')
def person(request, id):
    context = init(request, u'Страница пользователя')
    context['person'] = Person.objects.get(pk=id)
    return render(request, 'person.html', context)

@login_required(redirect_field_name='', login_url='/login/')
def meeting(request, id):
    context = init(request, u'Назначение встречи')
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            form.save(id)
            return HttpResponseRedirect(reverse('check'))
    else:
        form = MeetingForm()
    context['form'] = form
    return render(request, 'meeting.html', context)

@login_required(redirect_field_name='', login_url='/login/')
def fin_orders(request):
    content = init(request, u'Завершенные заказы', 'm5')
    content['orders'] = Order.objects.exclude(Status=u'В рассмотрении').order_by('-Date')
    return render(request, 'check.html', content)

@login_required(redirect_field_name='', login_url='/login/')
def check(request):
    content = init(request, u'Заказы', 'm4')
    content['orders'] = Order.objects.filter(Status=u'В рассмотрении').order_by('Date')
    return render(request, 'check.html', content)

@login_required(redirect_field_name='', login_url='/login/')
def index(request):
    context = init(request, u'Личный кабинет', 'm2')
    context['orders'] = Order.objects.filter(person=context['user']).order_by('Date')
    if len(context['orders']) != 0 and context['orders'][0].Status == u'Принято':
        meeting = Meeting.objects.filter(order=context['orders'][0])
        if len(meeting) != 0:
            context['meeting'] = meeting[0]
    return render(request, 'index.html', context)

@login_required(redirect_field_name='', login_url='/login/')
def new_order(request):
    context = init(request, u'Заказ', 'm3')
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(context['user'])
            return HttpResponseRedirect(reverse('account'))
    else:
        form = OrderForm()
    context['form'] = form
    return render(request, 'new_order.html', context)


def registration(request):
    context = init(request, u'Регистрация')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            f = form.save()
            login(request, f)
            return HttpResponseRedirect(reverse('account'))
    else:
        form = RegistrationForm()
    context['form'] = form
    return render(request, 'registration.html', context)


def log_in(request):
    context = init(request, 'Login')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.auth()
            login(request, user)
            return HttpResponseRedirect(reverse('account'))
    else:
        form = LoginForm()
    context['form'] = form
    return render(request, 'login.html', context)

@login_required(redirect_field_name='', login_url='/login/')
def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

@login_required(redirect_field_name='', login_url='/login/')
def account(request):
    context = init(request, u'Настройки', 'm1')
    print(context)
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect(reverse('account'))
    else:
        form = UserForm(initial={
            'Surname': context['user'].Surname,
            'Firstname': context['user'].Firstname,
            'GivenName': context['user'].GivenName,
            'Country': context['user'].Country,
            'State': context['user'].State,
            'Locality': context['user'].Locality,
            'StreetAddress': context['user'].StreetAddress,
            'email': context['user'].email,
            'INN': context['user'].INN,
            'SNILS': context['user'].SNILS})
    context['form'] = form
    return render(request, 'account.html', context)

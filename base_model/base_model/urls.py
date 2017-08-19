"""base_model URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.log_in, name='login'),
    url(r'^admin/', admin.site.urls),
    url(r'^account/', views.account, name='account'),
    url(r'^logout/', views.log_out, name='logout'),
    url(r'^registraion/', views.registration, name='registration'),
    url(r'^new_order/', views.new_order, name='new_order'),
    url(r'^check/', views.check, name='check'),
    url(r'^order/(\d+)/', views.order, name='order'),
    url(r'^person/(\d+)/', views.person, name='person'),
    url(r'^finorders/', views.fin_orders, name='finished_orders'),
    url(r'^meeting/(\d+)/', views.meeting, name='meeting')
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

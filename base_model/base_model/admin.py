from django.contrib import admin

from .models import Person, Order, Meeting

admin.site.register(Person)
admin.site.register(Order)
admin.site.register(Meeting)

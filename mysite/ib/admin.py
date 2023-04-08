from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Trade, Trade2
admin.site.register(Trade)
admin.site.register(Trade2)
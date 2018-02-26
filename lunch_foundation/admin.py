from django.contrib import admin

# Register your models here.
from .models import Event, Member, Cost

admin.site.register(Event)
admin.site.register(Member)
admin.site.register(Cost)

from django.contrib import admin
from .models import Imersionista, Ponto, Evento

# Register your models here.

admin.site.register(Imersionista)
admin.site.register(Ponto)
admin.site.register(Evento)
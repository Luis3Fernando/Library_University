from re import search
from django.contrib import admin
from .models import *

# Register your models here.

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ["id","user_name", "user_password"]
    search_fields = ["user_name"]

class CanalAdmin(admin.ModelAdmin):
    list_display = ["id","canal_code", "canal_name"]

class ArchivoAdmin(admin.ModelAdmin):
    list_display = ["titulo", "usuario", "canal"]

class ComentariosAdmin(admin.ModelAdmin):
    list_display = ["id","cm_texto", "cm_archivo"]

class MensajeAdmin(admin.ModelAdmin):
    list_display = ["id","ms_text", "ms_canal"]

class MembershipAdmin(admin.ModelAdmin):
    list_display = ["id","usuario", "canal"]

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Canal, CanalAdmin)
admin.site.register(Archivo, ArchivoAdmin)
admin.site.register(Comentarios)
admin.site.register(Mensaje, MensajeAdmin)
admin.site.register(Membership, MembershipAdmin)
from django.contrib import admin
from rbac import models
# Register your models here.

@admin.register(models.Userpurview)
class UserPurviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'show', 'name']
    list_editable = ['url', 'show', 'name']


@admin.register(models.Role)
class UserPurviewAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(models.Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'weight']

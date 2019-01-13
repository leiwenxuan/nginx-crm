from django.contrib import admin
from crm import models

# Register your models here.

admin.site.register(models.UserProfile)
admin.site.register(models.Campuses)
admin.site.register(models.ConsultRecord)
admin.site.register(models.StudyRecord)
admin.site.register(models.ContractTemplate)
admin.site.register(models.Enrollment)

@admin.register(models.ClassList)
class ClassListAdmin(admin.ModelAdmin):
    list_display = ('course', 'semester', 'campuses', 'price', 'show_campuses')
    list_display_links = ('campuses',)
    list_filter = ('price',)


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_filter = ('status', )







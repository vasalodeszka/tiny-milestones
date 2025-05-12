from django.contrib import admin

from apps.kids import models


@admin.register(models.Kid)
class KidAdmin(admin.ModelAdmin):
    list_display = ("full_name", "date_of_birth", "gender")
    list_filter = ("gender",)
    date_hierarchy = "date_of_birth"

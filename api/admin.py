from django.apps import apps
from django.contrib import admin


for model in apps.get_app_config('api').get_models():
    class OAdmin(admin.ModelAdmin):
        list_display = [field.name for field in model._meta.fields if field.name != "id"]
    admin.site.register(model,OAdmin)
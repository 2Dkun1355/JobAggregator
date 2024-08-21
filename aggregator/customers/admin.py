from django.contrib import admin
from .models import AdditionalUserFields


class AdditionalUserFieldsAdmin(admin.ModelAdmin):
    list_display = ['user', 'telegram_id', 'telegram_chat_id']
    list_filter = ['user']


admin.site.register(AdditionalUserFields, AdditionalUserFieldsAdmin)


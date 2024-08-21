from django.contrib import admin
from .models import AdditionalUserFields, UserSearch


class AdditionalUserFieldsAdmin(admin.ModelAdmin):
    list_display = ['user', 'telegram_id', 'telegram_chat_id']
    list_filter = ['user']


class UserSearchAdmin(admin.ModelAdmin):
    list_display = ['user', 'programming_language', 'location', 'is_remote',]
    list_filter = ['user', 'programming_language','salary', 'location',
                   'is_remote', 'level_need', 'years_need', 'english_lvl']


admin.site.register(AdditionalUserFields, AdditionalUserFieldsAdmin)
admin.site.register(UserSearch, UserSearchAdmin)
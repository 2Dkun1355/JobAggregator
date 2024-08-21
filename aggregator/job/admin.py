from django.contrib import admin
from .models import RawVacancy, Vacancy


class RawVacancyAdmin(admin.ModelAdmin):
    list_display = ['url', 'data']


class VacancyAdmin(admin.ModelAdmin):
    list_display = ['source', 'programming_language','level_need', 'salary', 'location', 'is_remote']
    list_filter = ['source', 'programming_language','level_need', 'salary', 'location', 'is_remote',
                   'years_need', 'english_lvl', 'update_date']


admin.site.register(RawVacancy,RawVacancyAdmin)
admin.site.register(Vacancy,VacancyAdmin)
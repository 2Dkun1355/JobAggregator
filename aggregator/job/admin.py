from django.contrib import admin
from .models import RawVacancy, Vacancy


class RawVacancyAdmin(admin.ModelAdmin):
    list_display = ['url', 'source', 'is_processed']
    list_filter = ['source', 'is_processed']


class VacancyAdmin(admin.ModelAdmin):
    list_display = ['source', 'programming_language','level_need', 'salary_min', 'salary_max', 'location', 'is_remote']
    list_filter = ['source', 'programming_language','level_need', 'salary_min', 'salary_max', 'location', 'is_remote',
                   'years_need', 'english_lvl', 'update_date']


admin.site.register(RawVacancy,RawVacancyAdmin)
admin.site.register(Vacancy,VacancyAdmin)
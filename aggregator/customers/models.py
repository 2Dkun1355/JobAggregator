from django.db import models
from django.contrib.auth.models import User

from job.models import Vacancy


class AdditionalUserFields(models.Model):
    user = models.OneToOneField(
        to=User,
        related_name='additional',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    telegram_id = models.CharField(
        max_length=64,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.id}'

class UserSearch(models.Model):
    user = models.ForeignKey(
        to=User,
        related_name='search',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    programming_language = models.CharField(max_length=32, null=True, blank=True)
    salary = models.IntegerField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    is_remote = models.BooleanField(null=True, blank=True)
    level_need = models.CharField(max_length=32, null=True, blank=True)
    years_need = models.IntegerField(null=True, blank=True)
    english_lvl = models.CharField(max_length=32, null=True, blank=True)
    vacancy = models.ManyToManyField(to='job.Vacancy', null=True, blank=True)

    def vacancy_match(self):
        fields = ['programming_language', 'location', 'level_need']
        filters = {}
        for field in fields:
            value = getattr(self, field)
            if value:
                filters.update({
                    field: value
                })

        vacancies = Vacancy.objects.filter(**filters)
        self.vacancy.set(vacancies)
        self.save()

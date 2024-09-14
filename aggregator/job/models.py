from django.db import models


class RawVacancy(models.Model):
    url = models.URLField(unique=True)
    data = models.TextField()
    is_processed = models.BooleanField(default=False)
    source = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return f'{self.source} - {self.url}'

class Vacancy(models.Model):
    source = models.CharField(max_length=32, null=True, blank=True)
    url = models.URLField()
    raw_data = models.OneToOneField(
        to=RawVacancy,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    description = models.TextField(null=True, blank=True)
    programming_language = models.CharField(max_length=32, null=True, blank=True)
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    is_remote = models.BooleanField(null=True, blank=True)
    level_need = models.CharField(max_length=32, null=True, blank=True)
    years_need = models.IntegerField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    english_lvl = models.CharField(max_length=32, null=True, blank=True)
    created_data = models.DateField(null=True, blank=True)
    parsing_data = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.source} - {self.url}'


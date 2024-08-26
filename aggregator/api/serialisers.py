from rest_framework import serializers

from job.models import RawVacancy, Vacancy


class RawVacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = RawVacancy
        fields = ['id', 'url', 'is_processed', 'source']


class VacancySerializer(serializers.ModelSerializer):
    raw_data = RawVacancySerializer()
    class Meta:
        model = Vacancy
        fields = ['id', 'source', 'url', 'raw_data', 'programming_language', 'location', 'is_remote', 'level_need',
                  'years_need', 'skills', 'created_data', 'parsing_data', 'update_date']

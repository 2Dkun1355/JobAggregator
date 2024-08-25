from rest_framework import serializers

from job.models import RawVacancy


class RawVacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = RawVacancy
        fields = ['id', 'url', 'is_processed', 'source']
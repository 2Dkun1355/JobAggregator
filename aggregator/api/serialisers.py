from datetime import datetime
from time import perf_counter

from django.contrib.auth import get_user_model

from rest_framework import serializers

from customers.models import AdditionalUserFields, UserSearch
from job.models import RawVacancy, Vacancy


UserModel = get_user_model()


class RawVacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = RawVacancy
        fields = ['id', 'url', 'is_processed', 'source']


class VacancySerializer(serializers.ModelSerializer):
    raw_data = RawVacancySerializer()
    salary_diff = serializers.SerializerMethodField(method_name='get_salary_diff', read_only=True, required=False)
    class Meta:
        model = Vacancy
        fields = ['id', 'source', 'url', 'raw_data', 'programming_language', 'location', 'is_remote', 'level_need',
                  'salary_min', 'salary_max', 'years_need', 'skills', 'created_data', 'parsing_data', 'update_date',
                  'salary_diff']

    @staticmethod
    def get_salary_diff(vacancy):
        if vacancy.salary_max and vacancy.salary_min:
            return vacancy.salary_max - vacancy.salary_min
        else:
            return None


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.update({
            'salary_diff': instance.salary_max - instance.salary_min
        })
        return representation


class VacancyChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = ['id', 'source', 'url', 'raw_data', 'programming_language', 'location', 'is_remote', 'level_need',
                  'years_need', 'skills', 'created_data', 'parsing_data', 'update_date']


class AdditionalUserFieldsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalUserFields
        fields = ['id', 'telegram_id', 'telegram_chat_id']

    def to_internal_value(self, data):
        internal = super().to_internal_value(data)
        # user = UserModel.objects.filter(is_superuser=True).first()
        # internal['user'] = user
        return internal


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.update({
            'created': datetime.now()
        })
        return representation


class UserSearchCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSearch
        fields = ['id', 'programming_language', 'salary', 'location',
              'is_remote', 'level_need', 'years_need', 'english_lvl']
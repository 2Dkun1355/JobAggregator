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
    city_category = serializers.SerializerMethodField(method_name='get_city_category', read_only=True, required=False)
    salary_match = serializers.SerializerMethodField(method_name='get_salary_match', read_only=True, required=False)
    class Meta:
        model = Vacancy
        fields = ['id', 'source', 'url', 'raw_data', 'programming_language', 'city_category', 'location', 'is_remote', 'level_need',
                  'salary_min', 'salary_max', 'salary_match', 'years_need', 'skills', 'created_data', 'parsing_data', 'update_date',
                  'salary_diff']

    @staticmethod
    def get_salary_diff(vacancy):
        if vacancy.salary_max and vacancy.salary_min:
            return vacancy.salary_max - vacancy.salary_min
        else:
            return None

    @staticmethod
    def get_city_category(vacancy):
        if vacancy.location:
            if vacancy.location in ['Lviv', 'Kyiv']:
                return 'Megapolis'
            else:
                return 'City'
        else:
            return None

    @staticmethod
    def get_salary_match(vacancy):
        if vacancy.years_need and vacancy.salary_max:
            default_salary = vacancy.years_need * 1000
            if vacancy.salary_max > 0 and default_salary > vacancy.salary_max * 1.2:
                return False
            return True

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
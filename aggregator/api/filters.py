import django_filters
from django.db.models import Q

from job.models import Vacancy
from customers.models import UserSearch

# показати  метод серіалайзер

class VacancyFilterSet(django_filters.FilterSet):
    years_need_min = django_filters.NumberFilter(field_name='years_need', lookup_expr='gte')
    years_need_max = django_filters.NumberFilter(field_name='years_need', lookup_expr='lte')
    for_junior = django_filters.BooleanFilter(method='filter_for_junior')
    best_vacancy = django_filters.BooleanFilter(method='filter_best_vacancy')

    class Meta:
        model = Vacancy
        fields = ['years_need_min', 'years_need_max', 'years_need', 'for_junior']

    def filter_best_vacancy(self, queryset, field_name, value):
        if value:
            try:
                if self.request.user.level == 'Junior':
                    return queryset.filter(Q(years_need__lte=1) | Q(level_need='Junior') | Q(salary_max__lte=1000))
                elif self.request.user.level == 'Middle':
                    return queryset.filter(Q(years_need__lte=2) | Q(level_need='Middle') | Q(salary_max__lte=1500))
            except:
                return queryset
        else:
            return queryset

    def filter_for_junior(self, queryset, field_name, value):
        if value:
            print('----11111')
            return queryset.filter(Q(years_need__lte=1) | Q(level_need='Junior') | Q(salary_max__lte=500))
        else:
            return queryset


class UserSearchFilterSet(django_filters.FilterSet):
    salary_start = django_filters.NumberFilter(field_name='salary', lookup_expr='gte')
    salary_end = django_filters.NumberFilter(field_name='salary', lookup_expr='lte')
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')
    programming_language_category = django_filters.CharFilter(method='get_programming_language_category')

    class Meta:
        model = UserSearch
        fields = ['programming_language', 'programming_language_category', 'salary', 'salary_start', 'salary_end', 'location', 'is_remote','level_need', 'years_need', 'english_lvl']

    def get_programming_language_category(self, queryset, field_name, value):
        if value == 'Top':
            return queryset.filter(Q(programming_language='Python') | Q(programming_language='Java'))
        elif value == 'Base':
            return queryset.filter(Q(programming_language='PHP') | Q(programming_language='Javascript'))
        return queryset
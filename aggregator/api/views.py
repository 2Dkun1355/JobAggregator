from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, filters
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.filters import VacancyFilterSet, UserSearchFilterSet
from api.serialisers import RawVacancySerializer, VacancySerializer, AdditionalUserFieldsCreateSerializer, \
    UserSearchCreateSerializer, VacancyChangeSerializer
from customers.models import AdditionalUserFields, UserSearch
from job.models import RawVacancy, Vacancy


class RawVacancyViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                        GenericViewSet):
    queryset = RawVacancy.objects.all()
    serializer_class = RawVacancySerializer
    permission_classes = [AllowAny]
    filterset_fields = ['source', 'is_processed']
    search_fields = ['data']
    ordering_fields = ['source', 'is_processed']


class VacancyViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                        GenericViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = [VacancySerializer, VacancyChangeSerializer]
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = VacancyFilterSet
    # filterset_fields = {
    #     'years_need': ['lte', 'gte']
    # }
    search_fields = ['skills', 'description']
    ordering_fields = ['level_need', 'years_need', 'created_data', 'parsing_data']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return VacancySerializer
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return VacancyChangeSerializer


class AdditionalUserFieldsViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                        GenericViewSet):
    queryset = AdditionalUserFields.objects.all()
    serializer_class = AdditionalUserFieldsCreateSerializer
    permission_classes = [AllowAny]
    filterset_fields = ['telegram_id', 'telegram_chat_id']


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)  # момент створення об'єкту в базі данних
        headers = self.get_success_headers(serializer.data)
        data = serializer.data
        data.update({
            'from_create': 'test'
        })
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class UserSearchViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                        GenericViewSet):
    queryset = UserSearch.objects.all()
    serializer_class = UserSearchCreateSerializer
    permission_classes = [AllowAny]
    filterset_class = UserSearchFilterSet
    ordering_fields = ['salary', 'location']
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny

from api.serialisers import RawVacancySerializer, VacancySerializer
from job.models import RawVacancy, Vacancy


class RawVacancyViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    queryset = RawVacancy.objects.all()
    serializer_class = RawVacancySerializer
    permission_classes = [AllowAny]


class VacancyViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = [AllowAny]
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny

from api.serialisers import RawVacancySerializer
from job.models import RawVacancy


class RawVacancyViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    queryset = RawVacancy.objects.all()
    serializer_class = RawVacancySerializer
    permission_classes = [AllowAny]


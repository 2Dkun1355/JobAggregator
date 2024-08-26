from rest_framework.routers import DefaultRouter

from api.views import RawVacancyViewSet, VacancyViewSet

router = DefaultRouter()
router.register('raw-vacancy', RawVacancyViewSet, basename='raw-vacancy'),
router.register('vacancy', VacancyViewSet, basename='vacancy')

urlpatterns = router.urls
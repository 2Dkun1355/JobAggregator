from rest_framework.routers import DefaultRouter

from api.views import RawVacancyViewSet, VacancyViewSet, AdditionalUserFieldsViewSet

router = DefaultRouter()
router.register('raw-vacancy', RawVacancyViewSet, basename='raw-vacancy'),
router.register('vacancy', VacancyViewSet, basename='vacancy')
router.register('user-additional', AdditionalUserFieldsViewSet, basename='user-additiona')

urlpatterns = router.urls
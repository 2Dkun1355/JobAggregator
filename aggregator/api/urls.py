from rest_framework.routers import DefaultRouter

from api.views import RawVacancyViewSet

router = DefaultRouter()
router.register('raw-vacancy', RawVacancyViewSet, basename='raw-vacancy'),


urlpatterns = router.urls
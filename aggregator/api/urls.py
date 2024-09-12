from rest_framework.routers import DefaultRouter

from api.views import RawVacancyViewSet, VacancyViewSet, AdditionalUserFieldsViewSet, UserSearchViewSet, UserViewSet

router = DefaultRouter()
router.register('raw-vacancy', RawVacancyViewSet, basename='raw-vacancy'),
router.register('vacancy', VacancyViewSet, basename='vacancy')
router.register('user-additional', AdditionalUserFieldsViewSet, basename='user-additional')
router.register('user-search', UserSearchViewSet, basename='user-search')
router.register('user', UserViewSet, basename='user')

urlpatterns = router.urls
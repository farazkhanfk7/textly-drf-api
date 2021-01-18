from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet,CheckAPI,GenAPI,TestAPI,SpellAPI

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('test/',TestAPI.as_view(),name="test"),
    path('check/',CheckAPI.as_view(),name="check"),
    path('generate/',GenAPI.as_view(),name="generate"),
    path('spell/',SpellAPI.as_view(),name="spell")
]
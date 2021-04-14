
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserCreate, CardViewSet


router = DefaultRouter()
router.register(r'card', CardViewSet)


urlpatterns = [
    path('register/', UserCreate.as_view()),
    path('', include(router.urls))
]

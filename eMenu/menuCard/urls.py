
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserCreate, CardViewSet, MealViewSet, UserLogIn

router = DefaultRouter()
router.register(r'card', CardViewSet, basename='card')
router.register(r'meal', MealViewSet)


urlpatterns = [
    path('register/', UserCreate.as_view()),
    path('login/', UserLogIn.as_view()),
    path('', include(router.urls))
]

from django.contrib.auth import authenticate, login
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Card, Meal
from .serializers import UserSerializer, MealSerializer, UserLogInSerializer, CardSerializerList, CardSerializerDetail, \
    CardSerializerMutate, MealSerializerCreate


# Create your views here.
class UserCreate(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(
        request=UserSerializer,
        responses={201: UserSerializer},
    )
    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogIn(APIView):

    @extend_schema(
        request=UserLogInSerializer
    )
    def post(self, request):
        serializer = UserLogInSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.data.get('username')
            password = serializer.data.get('password')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response()
        else:
            print("someone tried to login and failed!")
            print("Username: {} and password {}".format(username, password))
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CardViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'create_date', 'last_update']

    @extend_schema(
        request=CardSerializerMutate
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):

        ordering = request.query_params.get('order_by', 'title')
        if ordering in ['title', 'meals_counts']:
            queryset = self.get_queryset().order_by(ordering)
        else:
            queryset = self.get_queryset()

        serializer = self.get_serializer_class()(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'list':
            return CardSerializerList
        elif self.action in ['create', 'update', 'partial_update']:
            return CardSerializerMutate
        return CardSerializerDetail

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Card.objects.annotate(meals_counts=Count('meal'))
        else:
            return Card.objects.annotate(meals_counts=Count('meal')).filter(meals_counts__gt=0)


class MealViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Meal.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return MealSerializerCreate
        return MealSerializer

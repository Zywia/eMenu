from rest_framework import serializers

from .models import User, Card, Meal


class UserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    email = serializers.EmailField(
        required=True
    )
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)  # as long as the fields are the same, we can just use this
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserLogInSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'password')


class CardSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = Card
        depth = 1
        fields = "__all__"


class CardSerializerMutate(serializers.ModelSerializer):
    meal = serializers.PrimaryKeyRelatedField(many=True, write_only=True, queryset=Meal.objects.all())

    class Meta:
        model = Card
        fields = "__all__"


class CardSerializerList(serializers.ModelSerializer):
    meal = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'
    )

    class Meta:
        model = Card
        fields = ["id", "title", "description", "meal", "create_date", "last_update"]


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = "__all__"


class MealSerializerCreate(serializers.ModelSerializer):

    class Meta:
        model = Meal
        fields = ["id", "title", "description", "price", "time_to_prepare"]

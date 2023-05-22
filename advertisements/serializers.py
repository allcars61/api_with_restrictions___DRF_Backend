from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator', 'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания объявления."""

        # Получаем пользователя, создающего объявление
        user = self.context["request"].user

        # Проверяем, что у пользователя не больше 10 открытых объявлений
        if user.advertisement_set.filter(status="OPEN").count() >= 10:
            raise ValidationError({"detail": "У вас уже есть 10 открытых объявлений"})

        # Проставляем создателя объявления
        validated_data["creator"] = user

        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации при создании и обновлении объявления."""

        # Проверяем, что поле title не пустое
        if not data.get("title"):
            raise serializers.ValidationError("Поле 'title' обязательно для заполнения")

        return data
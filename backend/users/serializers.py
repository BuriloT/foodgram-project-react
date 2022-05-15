from django.forms import ValidationError
from rest_framework import serializers

from recipes.models import Subscribe, User


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'first_name', 'last_name', 'username', 'email', 'password',
            'is_subscribed'
        )
        model = User

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Subscribe.objects.filter(
            user=request.user, author=obj
        ).exists()

    def validate_email(self, data):
        if User.objects.filter(email=data).exists():
            raise ValidationError(
                'Пользователь с данной почтой уже существует!'
            )
        return data


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=150)
    current_password = serializers.CharField(max_length=150)

    def validate_current_password(self, data):
        user = self.context['request'].user
        current_password = data
        if not user.check_password(current_password):
            raise ValidationError('Неверный пароль, попробуйте еще раз')
        return current_password

    def validate(self, data):
        if data['current_password'] == data['new_password']:
            raise ValidationError('Пароли не должны совпадать!')
        return data

from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.fields import Base64ToImageField
from users.models import Match, User


class EmailPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        is_user_exists = User.objects.filter(email=data.get('email')).exists()
        if not is_user_exists:
            raise serializers.ValidationError({
                'email': 'Неверно указан адрес электронной почты.'
            })
        user = get_object_or_404(User, email=data.get('email'))
        if not user.check_password(data.get('password')):
            raise serializers.ValidationError({
                'password': 'Пароль неправильный.'
            })
        data['user'] = user
        return data


class SignupSerializer(serializers.ModelSerializer):
    avatar = Base64ToImageField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'avatar',
            'gender',
            'first_name',
            'last_name',
            'email',
            'password'
        )

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(
            validated_data.get('password')
        )
        return super().create(validated_data)


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ('user', 'candidate', 'like')

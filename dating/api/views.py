from math import atan, cos, radians, sin, sqrt

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.serializers import (EmailPasswordSerializer, MatchSerializer,
                             SignupSerializer)
from api.utils import get_integer_type, send_email
from users.models import Match, User

EARTH_RADIUS = 6371  # радиус Земли в километрах


@api_view(['POST'])
@permission_classes([AllowAny])
def create(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = EmailPasswordSerializer(
        data=request.data
    )
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data.get('user')
    token, created = Token.objects.get_or_create(user=user)
    return Response({'auth_token': token.key}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def logout(request):
    token = get_object_or_404(Token, user=request.user)
    token.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST', 'PATCH'])
def matching(request, client_id):
    user = request.user
    candidate = get_object_or_404(User, id=client_id)
    data = request.data
    is_like_exists = Match.objects.filter(
        user=user, candidate=candidate
    ).exists()
    if is_like_exists:
        match = Match.objects.get(user=user, candidate=candidate)
        serializer = MatchSerializer(match, data=data, partial=True)
    elif request.method == 'PATCH':
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        data['user'] = user.id
        data['candidate'] = candidate.id
        serializer = MatchSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    if is_like_exists and Match.objects.filter(
        user=candidate, candidate=user
    ).exists():
        user_like = Match.objects.get(user=user, candidate=candidate).like
        candidate_like = Match.objects.get(user=candidate, candidate=user).like
        if user_like and candidate_like:
            send_email(user.first_name, candidate.email)
            send_email(candidate.first_name, user.email)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('gender', 'first_name', 'last_name')
    search_fields = ('^first_name', '^last_name')

    def list(self, request):
        # filter_backends фильтруют queryset:
        queryset = self.filter_queryset(User.objects.all())
        # применяем getlist на случай, если distance содержится несколько раз:
        distance = request.query_params.getlist('distance')
        if distance == []:
            serializer = SignupSerializer(queryset, many=True)
            return Response(serializer.data)

        # проверка, что distance - натуральное число:
        distance = get_integer_type(distance[-1])  # берём последний параметр
        if distance is None or distance == 0:
            return Response(
                {'errors': 'distance должно быть натуральным числом'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # проверка: у клиента заданы координаты
        user = request.user
        user_lat, user_lng = user.latitude, user.longitude
        if user_lat is None or user_lng is None:
            return Response(
                {'errors': 'ваши координаты не заданы'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user_lat = radians(user_lat)
        user_lng = radians(user_lng)

        # Фильтрация по расстоянию.
        # извлечение координат пользователей:
        candidates = queryset.filter(
            latitude__isnull=False, longitude__isnull=False
        ).values('id', 'longitude', 'latitude')

        cos_user_lat = cos(user_lat)
        sin_user_lat = sin(user_lat)
        user_list = []
        for candidate in candidates:
            lat = radians(candidate.get('latitude'))
            lng = radians(candidate.get('longitude'))
            delta = abs(lng - user_lng)
            cos_lat = cos(lat)
            sin_lat = sin(lat)
            cos_delta = cos(delta)

            # вычисление расстояния до кандидата
            term_1 = cos_lat * sin(delta)
            term_2 = (
                cos_user_lat * sin_lat - sin_user_lat * cos_lat * cos_delta
            )
            divider = (
                sin_user_lat * sin_lat + cos_user_lat * cos_lat * cos_delta
            )
            central_angle = atan(sqrt(term_1**2 + term_2**2) / divider)
            candidate_distance = abs(central_angle) * EARTH_RADIUS

            if candidate_distance <= distance:
                user_list.append(candidate.get('id'))

        queryset = queryset.filter(id__in=user_list)
        serializer = SignupSerializer(queryset, many=True)
        return Response(serializer.data)

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.serializers import (EmailPasswordSerializer, MatchSerializer,
                             SignupSerializer)
from api.utils import send_email
from users.models import Match, User


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

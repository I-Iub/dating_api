from django.urls import include, path
from rest_framework import routers

from api.views import create, matching, login, logout, UserReadOnlyViewSet

router = routers.DefaultRouter()
router.register('list', UserReadOnlyViewSet, basename='users')

urlpatterns = [
    path('clients/create/', create, name='create'),
    path('clients/login/', login, name='login'),
    path('clients/logout/', logout, name='logout'),
    path('clients/<int:client_id>/match/', matching, name='match'),
    path('', include(router.urls)),
]

from django.urls import path

from api.views import create, login, logout

urlpatterns = [
    path('clients/create/', create, name='create'),
    path('clients/login/', login, name='login'),
    path('clients/logout/', logout, name='logout'),
]

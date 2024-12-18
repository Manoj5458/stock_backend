"""
Upstox URL Configuration

"""

from django.urls import path
from upstox.views import views
from .views.access_token_view import AccessTokenView 

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    # path('access-token', AccessTokenView.as_view(), name='access-token'),
    path('access-token', views.access_token, name='access-token'),
]
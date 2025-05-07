"""
Upstox URL Configuration

"""

from django.urls import path
from upstox.views.index_views import index
from upstox.views.auth_views import login, access_token, get_access_token, logout
from upstox.views.screener_views import screener

urlpatterns = [
    path('', index, name='index'),
    path('login', login, name='login'),
    path('access_token', access_token, name='access_token'),
    path('get_access_token', get_access_token, name='get_access_token'),
    path('logout', logout, name='logout'),
    path('screener', screener, name='screener'),
]
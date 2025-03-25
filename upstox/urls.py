"""
Upstox URL Configuration

"""

from django.urls import include, path
from upstox.views import views
from upstox.views.login_view import LoginView
from upstox.views.token_view import TokenView
path('upstox/', include('upstox.urls'))

urlpatterns = [
    path('', views.index, name='index'),
    # path('login', views.login, name='login'),
    path('access-token', TokenView.as_view(), name='access-token'),
    path('getAccessToken', TokenView.as_view(), name='get-access-token'),
    path('login', LoginView.as_view(), name='login'),
]
"""
upstox views
"""

# from django.http import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
# import upstox_client
import requests
from upstox_client.rest import ApiException

from upstox.config import API_KEY, REDIRECT_URI,API_SECRET

user_response = {}

# Create your views here.
def index(request):
    """index page"""
    return HttpResponse("Hello, world. You're at the upstox index.")
    
def get_access_token(request):
    print("Session Data:", request.session.items())
    user_id = request.session.get('user_id');
    print(f"user_id get access token: {user_id}");
    return JsonResponse({request.session.cookies.get('user_id')})
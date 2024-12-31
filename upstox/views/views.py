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

def login(request):
    auth_url = (
        f"https://api.upstox.com/v2/login/authorization/dialog"
        f"?response_type=code&client_id={API_KEY}&redirect_uri={REDIRECT_URI}"
    )
    return redirect(auth_url)

def access_token(request):
    code = request.GET.get("code")
    if code:
        return get_token(code)
    else:
        return HttpResponse("code" + code)
def get_token(code):
    # Prepare data for the API request
    data = {
        "client_id": API_KEY,
        "client_secret": API_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "code": code
    }
    
    url = 'https://api.upstox.com/v2/login/authorization/token'
    
    # Make the POST request to the Upstox API
    try:
        response = requests.post(url, data=data)
        # Check if the request was successful
        if response.status_code == 200:
            user_response.update(response.json()) 
            print(f"user_response {user_response}")           
            return HttpResponseRedirect('http://localhost:3000/upstox')
        else:
            api_response = response.json()
            error_message = api_response.get('errors', [])
            error_details = ", ".join([f"{error['errorCode']}: {error['message']}" for error in error_message])
            return HttpResponse(f"Error: {error_details}", status=response.status_code)
    
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Request failed: {str(e)}", status=500)
    
def get_access_token(request):
    request.session['access_token'] = user_response.get('access_token');
    return JsonResponse(user_response)
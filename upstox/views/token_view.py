from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
import requests

from upstox.config import API_KEY, API_SECRET, REDIRECT_URI


class TokenView(View):
    user_response = {}
    session = requests.Session()
    def get(self,request):
        code = request.GET.get("code")
        if not code:
            return HttpResponse("Invalid or missing code")
        return self.get_token(code,request)
    
    def get_token(self,code,request):
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
                # Get the access token from the response
                access_token = response.json().get('access_token')
                # Store the access token in the session
                request.session['access_token'] = access_token
                return HttpResponseRedirect('http://localhost:3000/upstox')
            else:
                api_response = response.json()
                error_message = api_response.get('errors', [])
                error_details = ", ".join([f"{error['errorCode']}: {error['message']}" for error in error_message])
                return HttpResponse(f"Error: {error_details}", status=response.status_code)
        
        except requests.exceptions.RequestException as e:
            return HttpResponse(f"Request failed: {str(e)}", status=500)

    def get_access_token(response):
        access_token = response.json().get('access_token');
        print(access_token);
        return access_token


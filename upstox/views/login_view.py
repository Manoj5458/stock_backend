from django.shortcuts import redirect
from django.views import View
from upstox.config import API_KEY, REDIRECT_URI


class LoginView(View):
    def get(self,request):
        auth_url = (
            f"https://api.upstox.com/v2/login/authorization/dialog"
            f"?response_type=code&client_id={API_KEY}&redirect_uri={REDIRECT_URI}"
        )
        return redirect(auth_url)
    
    # redirect url : http://localhost:8000/upstox/access-token
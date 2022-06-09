from django.urls import path
from .views import SignUpView

app_name = 'accounts'
urlpatterns = [
    # e.g. /account/signup/ to view the signup page
    path("signup/", SignUpView.as_view(), name="signup")
]
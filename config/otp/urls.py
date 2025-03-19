from django.urls import path
from .views import SignupView, VerifyOTPView, home_view

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('verify/', VerifyOTPView.as_view(), name='verify_otp'),
    path('', home_view, name='home'),
]

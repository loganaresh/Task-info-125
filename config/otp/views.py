from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views import View
from .models import OTP
from .forms import PhoneForm, OTPForm
from django.conf import settings
from twilio.rest import Client
import random

# Twilio Credentials
TWILIO_ACCOUNT_SID = 'your_twilio_account_sid'
TWILIO_AUTH_TOKEN = 'your_twilio_auth_token'
TWILIO_PHONE_NUMBER = 'your_twilio_phone_number'

# Send OTP Function
def send_otp(phone_number):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    otp = str(random.randint(100000, 999999))
    OTP.objects.update_or_create(phone_number=phone_number, defaults={'otp': otp})
    message = client.messages.create(
        body=f'Your OTP is {otp}',
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return otp

# Signup View
class SignupView(View):
    def get(self, request):
        form = PhoneForm()
        return render(request, 'signup.html', {'form': form})
    
    def post(self, request):
        form = PhoneForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            send_otp(phone_number)
            request.session['phone_number'] = phone_number
            return redirect('verify_otp')
        return render(request, 'signup.html', {'form': form})

# OTP Verification View
class VerifyOTPView(View):
    def get(self, request):
        form = OTPForm()
        return render(request, 'verify_otp.html', {'form': form})
    
    def post(self, request):
        form = OTPForm(request.POST)
        phone_number = request.session.get('phone_number')
        if form.is_valid() and phone_number:
            otp = form.cleaned_data['otp']
            otp_obj = OTP.objects.filter(phone_number=phone_number, otp=otp).first()
            if otp_obj:
                user, created = get_user_model().objects.get_or_create(phone_number=phone_number)
                user.is_verified = True
                user.save()
                messages.success(request, 'Phone number verified successfully!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid OTP')
        return render(request, 'verify_otp.html', {'form': form})
def home_view(request):
    return render(request, 'home.html')
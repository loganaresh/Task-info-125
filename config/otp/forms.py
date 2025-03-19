from django import forms

class PhoneForm(forms.Form):
    phone_number = forms.CharField(max_length=15, required=True)

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6, required=True)

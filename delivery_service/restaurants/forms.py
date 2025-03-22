from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, DeliveryAddress

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone', 'avatar')

class AddressForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddress
        fields = ('city', 'street', 'house', 'apartment', 'comment')
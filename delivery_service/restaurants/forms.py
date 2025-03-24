from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, DeliveryAddress, UserAddress

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
        model = UserAddress
        fields = ['city', 'street', 'house', 'apartment', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    phone = forms.CharField(max_length=20, required=False, label='Телефон')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'password1', 'password2')
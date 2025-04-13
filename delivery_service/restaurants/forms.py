from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, UserAddress, CartItem

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
        fields = ['city', 'street', 'house', 'apartment', 'entrance', 'floor', 'comment']
        widgets = {
            'city': forms.TextInput(attrs={
                'placeholder': 'Москва',
                'class': 'form-control'
            }),
            'street': forms.TextInput(attrs={
                'placeholder': 'ул. Ленина',
                'class': 'form-control'
            }),
            'house': forms.TextInput(attrs={
                'placeholder': '12', 
                'class': 'form-control'
            }),
            'apartment': forms.TextInput(attrs={
                'placeholder': '34 (необязательно)',
                'class': 'form-control'
            }),
            'entrance': forms.TextInput(attrs={
                'placeholder': 'Подъезд (необязательно)',
                'class': 'form-control'
            }),
            'floor': forms.TextInput(attrs={
                'placeholder': 'Этаж (необязательно)',
                'class': 'form-control'
            }),
            'comment': forms.Textarea(attrs={
                'placeholder': 'Код домофона, цвет двери и т.д.',
                'rows': 3,
                'class': 'form-control'
            }),
        }

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    phone = forms.CharField(max_length=20, required=False, label='Телефон')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'password1', 'password2')

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity', 'special_requests']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1, 'class': 'form-control'}),
            'special_requests': forms.Textarea(attrs={'rows': 2}),
        }

class CustomAuthForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Неверный логин или пароль, или данного пользователя не существует",
        'inactive': "Аккаунт деактивирован",
    }


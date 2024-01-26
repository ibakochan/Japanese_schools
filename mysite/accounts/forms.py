from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    # A signupform Using djangos built in UserCreationForm requiring username password and password confirmation.
    # Using widget to make the input form nice and uniform.

    username = forms.CharField(
        label="名前",
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    password1 = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    password2 = forms.CharField(
        label="パスワード確認",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2')

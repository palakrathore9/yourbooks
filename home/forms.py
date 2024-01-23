from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already in use. Please choose a different one.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use. Please use a different one.')
        return email

class UserProfileUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_username(self):
        username = self.cleaned_data['username']
        current_user = self.instance
        if User.objects.exclude(pk=current_user.pk).filter(username=username).exists():
            raise forms.ValidationError('This username is already in use. Please choose a different one.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        current_user = self.instance
        if User.objects.exclude(pk=current_user.pk).filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use. Please use a different one.')
        return email


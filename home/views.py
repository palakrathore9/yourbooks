from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate
from .forms import UserProfileUpdateForm
from django.contrib.auth.models import User
from django.contrib.messages import success



def index(request):
    all_registered_users = User.objects.all() 
    return render(request, 'index.html', {'all_registered_users': all_registered_users})


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)

            return redirect('index')

    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            success(request, 'Profile updated successfully!')
            return redirect('index')
        else:
            messages.error(request, 'Error updating profile. Please check the form.')

    else:
        form = UserProfileUpdateForm(instance=request.user)

    return render(request, 'update_profile.html', {'form': form})


def custom_logout(request):
    logout(request)
    return redirect('index') 

class CustomLoginView(LoginView):
    template_name = 'login.html'  

    def get_success_url(self):
        return '/'  

    def form_valid(self, form):
        return super().form_valid(form)
    
    def get(self, request, *args, **kwargs):
        custom_message = request.GET.get('message', None)
        return render(request, 'login.html', {'custom_message': custom_message})
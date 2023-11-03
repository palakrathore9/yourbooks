
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import pickle
import numpy as np
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib import messages

popular_df = pickle.load( open('home/popular.pkl', 'rb'))
pt = pickle.load(open('home/pt.pkl', 'rb'))
books = pickle.load(open('home/books.pkl', 'rb'))
similarity_scores = pickle.load(open('home/similarity_scores.pkl', 'rb'))

def index(request):
    popular_df.columns = popular_df.columns.str.replace('-', '_')
    book_data = popular_df.to_dict(orient='records')
    return render(request, 'index.html', {'book_data': book_data})


def recommend_ui(request):
    return render(request, 'recommend.html')

def recommend(request):
    data = []
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '').lower() 
         # Convert to lowercase for case-insensitive search
        if not request.user.is_authenticated:
            message = "Login required to get book recommendations."
            return redirect(f'/login/?message={message}')
        try:
            # Search for the input in a case-insensitive manner
            index = np.where(pt.index.str.lower() == user_input)[0]
            index=index[0]
            similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

            for i in similar_items:
                item = []
                temp_df = books[books['Book-Title'] == pt.index[i[0]]]
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

                data.append(item)
        except IndexError:
            error_message = "Book not found in the dataset. Please try a different book."
            return render(request, 'recommend.html', {'error_message': error_message,})

    return render(request, 'recommend.html', {'data': data})
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
def custom_logout(request):
    logout(request)
    return redirect('index') 

class CustomLoginView(LoginView):
    template_name = 'login.html'  # Specify your custom login template

    def get_success_url(self):
        return '/'  # Redirect to the home page after login

    def form_valid(self, form):
        # Customize login logic if needed
        return super().form_valid(form)
    def get(self, request, *args, **kwargs):
        custom_message = request.GET.get('message', None)
        return render(request, 'login.html', {'custom_message': custom_message})
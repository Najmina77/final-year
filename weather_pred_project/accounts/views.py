from django.shortcuts import render
from django.contrib.auth import login, logout,authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.views.generic import CreateView

from .models import User, Farmer, Farmers
from .form import FarmerSignUpForm
# Create your views here.

# home page
def landing_page_view(request):
    return render(request, "../templates/landing_page.html")


# login
@csrf_exempt
def login_request(request):

    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request,user)
                # if credentials match an applicant, redirect to farmer's dashboard
                if user.is_farmer == True :
                    print(user)
                    return redirect('/st-farmer')
                # if credentials match an admin account, redirect to admin dashboard
                if user.is_admin == True or user.is_superuser == True:
                    return redirect('/ds-admin/')
                
                
            else:
                messages.error(request,"Invalid USERNAME or PASSWORD")
        else:
                messages.error(request,"Invalid USERNAME or password")
    return render(request, '../templates/login.html',
    context={'form':AuthenticationForm()})

# when you  log out, be redirected to the login page
@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect('/login/')

# Register
class register(CreateView):
    model = User
    form_class = FarmerSignUpForm
    template_name = '../templates/register.html'

    # redirect to login page after successful login
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/login/')

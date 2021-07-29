from django.shortcuts import render
from django.contrib.auth import login, logout,authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.views.generic import CreateView
import pickle
import pandas as pd

from .models import User, Farmer, Farmers
from .form import FarmerSignUpForm, CityForm
# Create your views here.

# home page
def landing_page_view(request):
    return render(request, "../templates/landing_page.html")


# login
@csrf_exempt
def login_request(request):

    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        city_form = CityForm()
        form_context = { 'form' : city_form}
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request,user)
                # if credentials match an applicant, redirect to farmer's dashboard
                if user.is_farmer == True :
                    print(user)
                    return redirect('/weather_stations', form)
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

# login
@csrf_exempt
def get_city_weather(request):
    if request.method == "POST":
        form = CityForm(request.POST)

        if form.is_valid():

            #get cleaned form data, process something and return it to the user            
            city_name = form.cleaned_data.get('city')
            date = form.cleaned_data.get('date')
            message = predict_weather(city_name.capitalize(), date)
            return render(request, '../templates/menubar.html', {'form': form, 'message': message})

    else:
        form = CityForm()
    
    return render(request, '../templates/menubar.html', {'form': form})



def predict_weather(city, date):
    # load the embu model and try predicting
   
    if city == 'Nyeri':
        nyeri_weather_model = pickle.load(open(r'C:\Users\humph\Desktop\Folder\Najma\final-year\weather_pred_project\accounts\ml_models\nyeri_weather_model', 'rb'))
        pred = nyeri_weather_model.get_prediction(start=pd.to_datetime(date), dynamic=False)
        pred_ci = pred.conf_int()
        low_temp = pred_ci['lower temp_actual'].tolist()[0]
        high_temp = pred_ci['upper temp_actual'].tolist()[0] 
        mean_temp = (low_temp + high_temp)/2
        return  'The lowest temp : {}, the highest temp  : {}, and the mean temp : {}, both in degrees celcius'.format(low_temp, high_temp, mean_temp)
        

    elif city == 'Embu':
        nyeri_weather_model = pickle.load(open(r'C:\Users\humph\Desktop\Folder\Najma\final-year\weather_pred_project\accounts\ml_models\embu_weather_model', 'rb'))
        pred = nyeri_weather_model.get_prediction(start=pd.to_datetime(date), dynamic=False)
        pred_ci = pred.conf_int()
        low_temp = pred_ci['lower temp_actual'].tolist()[0]
        high_temp = pred_ci['upper temp_actual'].tolist()[0] 
        mean_temp = (low_temp + high_temp)/2
        return 'The lowest temp : {}, the highest temp  : {}, and the mean temp : {}, both in degrees celcius'.format(low_temp, high_temp, mean_temp)
        
    

    elif city =='Nanyuki':
        nanyuki_weather_model= pickle.load(open(r'C:\Users\humph\Desktop\Folder\Najma\final-year\weather_pred_project\accounts\ml_models\nanyuki_weather_model', 'rb'))
        pred = nanyuki_weather_model.get_prediction(start=pd.to_datetime(date), dynamic=False)
        pred_ci = pred.conf_int()
        low_temp = pred_ci['lower temp_actual'].tolist()[0]
        high_temp = pred_ci['upper temp_actual'].tolist()[0] 
        mean_temp = (low_temp + high_temp)/2
        return 'The lowest temp : {}, the highest temp  : {}, and the mean temp : {} , both in degrees celcius'.format(low_temp, high_temp, mean_temp)
        
    else:
        return 'Hi, unfortunately the Data for {} is not available now, we are working on it'.format(city)

     
    
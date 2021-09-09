from django.shortcuts import render
from django.contrib.auth import login, logout,authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.views.generic import CreateView
import pickle
import pandas as pd
import array

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
                    # return redirect('/weather_stations', form)
                    return redirect('/get_weather/')
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

# predict and return message
@csrf_exempt
def get_city_weather(request):
    if request.method == "POST":
        form = CityForm(request.POST or None)

        if form.is_valid():
            valid_data = form.save(commit=False)

            #get cleaned form data, process something and return it to the user            
            valid_data.city_name = form.cleaned_data.get('city')
            valid_data.date = form.cleaned_data.get('date')
            # save this data to the database, in the CityWeather table
            valid_data.save
            temp, precip, crop = predict_weather(valid_data.city_name.capitalize(), valid_data.date)
            return render(request, '../templates/menubar.html', {'form': form, 'temp': temp, 'precip':precip, 'crop':crop})

    else:
        form = CityForm()
    
    return render(request, '../templates/menubar.html', {'form': form})

    # C:\Users\Najmina\Desktop\Najma Nalka\final-year\cc-frontend> 

# ng build --prod --output-path ../../../najma_final_proj/final_year/weather_pred_project/weather_pred_project/accounts/static/ang --watch --output-hashing none

# function to predict weather given the city and date information
def predict_weather(city, date):
    # load the embu model and try predicting
   
    if city == 'Nyeri':
        # load the ml prediction file
        nyeri_weather_model = pickle.load(open(r"C:\Users\humph\Desktop\najma_final_proj\final-year\Intelligence\nyeri_weather_model", 'rb'))
        nyeri_weather_model_prep = pickle.load(open(r"C:\Users\humph\Desktop\najma_final_proj\final-year\Intelligence\nyeri_weather_model_prep",'rb'))

        pred = nyeri_weather_model.get_prediction(start=pd.to_datetime(date), dynamic=False)
        pred_precp = nyeri_weather_model_prep.get_prediction(start=pd.to_datetime(date), dynamic=False)


        pred_ci = pred.conf_int()
        pred_ci_precp = pred_precp.conf_int()

       
        # get low temperature value
        low_temp = pred_ci['lower temp_actual'].tolist()[0]
        lower_prep = pred_ci_precp['lower precipitation_actual'].tolist()[0]

        # get max temp value
        high_temp = pred_ci['upper temp_actual'].tolist()[0] 
        higher_prep = pred_ci_precp['upper precipitation_actual'].tolist()[0]

        # get mean temperature value
        mean_temp = (low_temp + high_temp)/2
        avg_precp = (lower_prep + higher_prep)/2

        
        # get precipitattion test
        # = pred_ci['lower precipitation'
        temp = 'Lowest temp : {} \n Highest temp  : {} \n Average temp : {}\n'.format(low_temp, high_temp, mean_temp)
        precip = 'Lowest  relative humidity : {} \n Highest relative humidity  : {} \n Average  relative humidity : {} \n'.format(lower_prep, higher_prep,  avg_precp)
        predict_value =  '' # this value will be replaced later upon calculation
         
        return (temp, precip, predict_value)
        

    elif city == 'Embu':
        # embu_precipitation_model_name = pickle.load(open(r"C:\Users\Najmina\Desktop\najma_final_proj\final-year\Intelligence\embu_precipitation_model_name", 'rb'))
        nyeri_weather_model = pickle.load(open(r"C:\Users\humph\Desktop\najma_final_proj\final-year\Intelligence\embu_weather_model", 'rb'))
        embu_weather_model_prep = pickle.load(open(r"C:\Users\humph\Desktop\najma_final_proj\final-year\Intelligence\embu_weather_model_prep", 'rb'))
  
        pred = nyeri_weather_model.get_prediction(start=pd.to_datetime(date), dynamic=False)
        pred_precp = embu_weather_model_prep.get_prediction(start=pd.to_datetime(date), dynamic=False)

        pred_ci = pred.conf_int()
        pred_ci_precp = pred_precp.conf_int()

       
        # get low temperature value
        low_temp = pred_ci['lower temp_actual'].tolist()[0]
        lower_prep = pred_ci_precp['lower precipitation_actual'].tolist()[0]

        # get max temp value
        high_temp = pred_ci['upper temp_actual'].tolist()[0] 
        higher_prep = pred_ci_precp['upper precipitation_actual'].tolist()[0]

        # get mean temperature value
        mean_temp = (low_temp + high_temp)/2
        avg_precp = (lower_prep + higher_prep)/2

        
        # get precipitattion test
        # = pred_ci['lower precipitation'
        temp = 'Lowest temp : {} \n Highest temp  : {} \n Average temp : {} \n'.format(low_temp, high_temp, mean_temp)
        precip = 'Lowest  relative humidity : {} \n Highest relative humidity  : {} \n Average  relative humidity : {} \n'.format(lower_prep, higher_prep,  avg_precp)
        predict_value =  '' # this value will be replaced later upon calculation
         
        return (temp, precip, predict_value)
     


    elif city =='Nanyuki':
        nanyuki_weather_model= pickle.load(open(r"C:\Users\humph\Desktop\najma_final_proj\final-year\Intelligence\nayuki_weather_model", 'rb'))
        nanyuki_weather_model_prep= pickle.load(open(r"C:\Users\humph\Desktop\najma_final_proj\final-year\Intelligence\nayuki_weather_model_prep", 'rb'))
        
        pred_precp = nanyuki_weather_model_prep.get_prediction(start=pd.to_datetime(date), dynamic=False)
        pred = nanyuki_weather_model.get_prediction(start=pd.to_datetime(date), dynamic=False)

        pred_ci = pred.conf_int()
        pred_ci_precp = pred_precp.conf_int()

        # get low temperature value
        low_temp = pred_ci['lower temp_actual'].tolist()[0]
        lower_prep = pred_ci_precp['lower precipitation_actual'].tolist()[0]

        # get max temp value
        high_temp = pred_ci['upper temp_actual'].tolist()[0] 
        higher_prep = pred_ci_precp['upper precipitation_actual'].tolist()[0]

        # get mean temperature value
        mean_temp = (low_temp + high_temp)/2
        avg_precp = (lower_prep + higher_prep)/2

        
        # get precipitattion test
        # = pred_ci['lower precipitation'
        temp = 'Lowest temp : {} \n Highest temp  : {} \n Average temp : {} \n'.format(low_temp, high_temp, mean_temp)
        precip = 'Lowest  relative humidity : {} \n Highest relative humidity  : {} \n Average  relative humidity : {} \n'.format(lower_prep, higher_prep,  avg_precp)
        predict_value =  '' # this value will be replaced later upon calculation
         
        return (temp, precip, predict_value)
        
    else:
        temp = 'Hi, unfortunately the temperature for {} is not available now, we are working on it'.format(city)
        precip = 'Hi, unfortunately the relative humidity for {} is not available now, we are working on it'.format(city)
        crop = 'Hi, unfortunately the Data for {} is not available now, we are working on it'.format(city)
        return (temp, precip,  crop)

     
    
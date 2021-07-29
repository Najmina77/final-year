from django.contrib.auth.forms import UserCreationForm
from django.db import models, transaction
from django import forms
from django.db.models import fields
from django.forms.models import ModelForm
from .models import CityWeather, User, Farmer, Farmers

class FarmerSignUpForm(UserCreationForm):
    # applicant_full_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Please enter full name'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Please enter first name'}))
    middle_name = forms.CharField(required=True, widget= forms.TextInput(attrs={'placeholder': 'Enter middle name'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter last name'}))
    # id_number = forms.IntegerField(required=True)
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Enter email'}))
    phone = forms.CharField(required=True, widget=forms.NumberInput(attrs={'placeholder': 'Enter phone number'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'required': 'required'}))

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic

    def save(self):
        user = super().save(commit=False)
        user.is_farmer = True
        user.first_name = self.cleaned_data.get('first_name')
        user.middle_name = self.cleaned_data.get('middle_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()

        farmer = Farmers.objects.create(user=user)
        farmer.first_name = self.cleaned_data.get('first_name')
        farmer.middle_name = self.cleaned_data.get('middle_name')
        farmer.last_name = self.cleaned_data.get('last_name')
        farmer.email = self.cleaned_data.get('email')
        farmer.phone = self.cleaned_data.get('phone')
        farmer.date_of_birth = self.cleaned_data.get('date_of_birth')
        farmer.save()

        return user



class CityForm(ModelForm):
    class Meta:
        model =  CityWeather
        fields = '__all__'


    


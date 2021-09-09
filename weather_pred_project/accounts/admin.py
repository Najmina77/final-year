from django.contrib import admin
from .models import User, Farmer, Farmers, CityWeather
# Register your models here.

admin.site.register(User)
admin.site.register(Farmer)
admin.site.register(Farmers)
admin.site.register(CityWeather)
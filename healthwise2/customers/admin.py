from django.contrib import admin
from .models import DailyIntake, FoodItem

# Register your models here.
admin.site.register(DailyIntake)
admin.site.register(FoodItem)

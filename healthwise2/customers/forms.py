from django import forms
from .models import DailyIntake, FoodItem, Goal
from django.forms import inlineformset_factory

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['food', 'fats', 'carbs', 'protein']

class BMICalculatorForm(forms.Form):
    weight = forms.FloatField()
    height_feet = forms.IntegerField()
    height_inches = forms.IntegerField()


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['calorie']

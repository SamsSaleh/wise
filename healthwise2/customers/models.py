from django.db import models
from accounts.models import User

# Create your models here.

class DailyIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    calorie = models.IntegerField()


class FoodItem(models.Model):
    food = models.CharField(max_length=100)
    fats = models.FloatField()
    carbs = models.FloatField()
    protein = models.FloatField()
    calorie = models.ForeignKey(DailyIntake, on_delete=models.CASCADE)

    def __str__(self):
        return self.food


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    calorie = models.IntegerField()
      
    def __str__(self):
        return self.goal


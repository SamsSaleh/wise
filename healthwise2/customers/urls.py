from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('reddit_posts/', views.reddit_posts, name='reddit_posts'),
    path('profile/', views.profile, name='profile'),
    path('daily_intake/', views.daily_intake, name='daily_intake'),
    path('show_daily_intake/<int:pk>/', views.show_daily_intake, name='show_daily_intake'),
    path('calculate-bmi/', views.calculate_bmi, name='calculate_bmi'),
    path('set_goal/', views.set_goal, name='set_goal'),

]

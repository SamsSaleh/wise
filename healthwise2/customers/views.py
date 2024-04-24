from django.shortcuts import render, redirect
import praw
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from .forms import FoodItemForm, BMICalculatorForm, GoalForm
from django.forms import formset_factory
from .models import DailyIntake, FoodItem, Goal
from django.contrib import messages
from .utils import calculate_calories
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json

# Create your views here.

def home(request):
    queryset = DailyIntake.objects.filter(user=request.user)
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 3)
    try:
        paginated_items = paginator.page(page)
    except PageNotAnInteger:
        paginated_items = paginator.page(1)
    except EmptyPage:
        paginated_items = paginator.page(paginator.num_pages)
    
    # graph data
    dates = [obj.date for obj in queryset]
    # convert date to string
    dates = [date.strftime('%Y-%m-%d') for date in dates]
    # create a list from the queryset as sum of all items from each daily intake
    calories = [sum([item.fats + item.carbs + item.protein for item in obj.fooditem_set.all()]) for obj in queryset]
    goal = Goal.objects.filter(user=request.user).last()
    
    if not goal:
        goal = Goal.objects.create(user=request.user, calorie=2000)
    
    graph_data = {
        'dates': dates,
        'calories': calories,
        'goal': goal.calorie
    }
    # dump the data to json
    graph_data = json.dumps(graph_data)
    return render(request, 'customers/home.html', {'paginated_items': paginated_items, 'graph_data': graph_data})

def reddit_posts(request):
    reddit = praw.Reddit(
        client_id=settings.REDDIT_CLIENT_ID,
        client_secret=settings.REDDIT_CLIENT_SECRET,
        user_agent=settings.REDDIT_USER_AGENT,
        username=settings.REDDIT_USERNAME,
        password=settings.REDDIT_PASSWORD
    )
    subreddit = reddit.subreddit('Nutrition')
    posts = subreddit.hot(limit=10)  # Fetch the top 10 hot posts from the Django subreddit

    context = {'posts': posts}

    list_of_posts = []
    for post in posts:
        dic = {}
        dic['title'] = str(post.title)
        dic['url'] = str(post.url)
        dic['author'] = str(post.author)

        list_of_posts.append(dic)

    return JsonResponse(list_of_posts, safe=False)

def profile(request):
    return render(request, 'customers/profile.html')

def daily_intake(request):
    calory_formset = formset_factory(FoodItemForm, extra=2)

    if request.method == 'POST':
        formset = calory_formset(request.POST)
        if formset.is_valid():
            daily_intake = DailyIntake.objects.create(user=request.user, calorie=calories(formset))
            for form in formset:
                food_item = form.save(commit=False)
                food_item.calorie = daily_intake
                food_item.save()
            messages.success(request, 'Your daily intake was saved successfully!')
            return redirect('daily_intake')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        formset = calory_formset()
    return render(request, 'customers/daily_intake.html', {'formset': formset})

def calories(formset):
    calories = 0
    for form in formset:
        fats = form.cleaned_data.get('fats')
        carbs = form.cleaned_data.get('carbs')
        protein = form.cleaned_data.get('protein')
        calories += calculate_calories(fats, carbs, protein)
    return calories

def show_daily_intake(request, pk):
    daily_intake = DailyIntake.objects.get(pk=pk)
    food_items = FoodItem.objects.filter(calorie=daily_intake)
    return render(request, 'customers/show_daily_intake.html', {'daily_intake': daily_intake, 'food_items': food_items})

def calculate_bmi(request):
    if request.method == 'POST':
        form = BMICalculatorForm(request.POST)
        if form.is_valid():
            weight = form.cleaned_data.get('weight') # in kg
            height_feet = form.cleaned_data.get('height_feet')
            height_inches = form.cleaned_data.get('height_inches')
            height = (height_feet * 12) + height_inches
            bmi = calculate_bmi_func(weight, height)
            return render(request, 'customers/bmi_result.html', {'bmi': bmi})
    else:
        form = BMICalculatorForm()
    return render(request, 'customers/bmi_calculator.html', {'form': form})

def calculate_bmi_func(weight, height):
    bmi = (weight / (height * height)) * 703
    return round(bmi, 1)


def set_goal(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, 'Your goal was saved successfully!')
            return redirect('set_goal')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = GoalForm()
    return render(request, 'customers/set_goal.html', {'form': form})


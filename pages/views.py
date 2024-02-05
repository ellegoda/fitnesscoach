from django.db.models.functions import TruncWeek, TruncMonth
from django.shortcuts import render, redirect
from allauth.account.views import SignupView
from .forms import CustomSignupForm, ActivityForm
from .models import DietPlan, ActivityProgram, Activity
from datetime import datetime, timedelta
from django.db.models import Sum, F

class CustomSignupView(SignupView):
    form_class = CustomSignupForm
    success_url = '/dashboard/'


def index(request):
    return render(request, "index.html")


def get_user_bmi(user):
    if user.is_authenticated and hasattr(user, 'bmi'):
        return user.bmi
    return None


def get_user_goal(user):
    if user.is_authenticated and hasattr(user, 'bmi'):
        return user.daily_calories_burn_goal
    return 0


def create_activity(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('dashboard')
    else:
        form = ActivityForm()
    return render(request, 'dashboard.html', {'activity_form': form})


def calculate_weekly_calories(user):
    # Calculate the start and end date of the current week
    today = datetime.today()
    start_date = today - timedelta(days=today.weekday())
    end_date = start_date + timedelta(days=6)

    # Filter activities for the current week
    weekly_activities = (
        Activity.objects
        .filter(user=user, date__range=[start_date, end_date])
        .annotate(calories_burned=F('duration_minutes') * (
                    F('activity_type__calories_burn') / F('activity_type__unit_duration_minutes')))
    )

    # Calculate the total calories burned for the week
    total_calories = weekly_activities.aggregate(Sum('calories_burned'))[
        'calories_burned__sum']

    return round(total_calories) or 0


def monthly_calories(user):
    monthly_report = (
        Activity.objects
        .filter(user=user)
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total_calories=Sum(
            F('duration_minutes') * (F('activity_type__calories_burn') / F('activity_type__unit_duration_minutes'))))
        .order_by('month')
    )

    # Create data for Chart.js
    chart_data = {
        'labels': [month['month'].strftime('%B') for month in monthly_report],
        'datasets': [{
            'label': 'Total Calories Burned',
            'data': [month['total_calories'] for month in monthly_report],
            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
            'borderColor': 'rgba(75, 192, 192, 1)',
            'borderWidth': 1,
            'fill': False,
        }],
    }

    return chart_data


def dashboard(request):
    user_bmi = get_user_bmi(request.user)
    user_goal = get_user_goal(request.user)
    weekly_calories = calculate_weekly_calories(request.user)
    calories_goal_progress = (weekly_calories / 7000) * 100
    activity_programs = ActivityProgram.objects.filter(bmi_from__lte=user_bmi, bmi_to__gte=user_bmi)
    diet_plans = DietPlan.objects.filter(bmi_from__lte=user_bmi, bmi_to__gte=user_bmi)
    initial_data = {'date': datetime.today()}
    activity_form = ActivityForm(initial=initial_data)
    monthly_report = monthly_calories(request.user)

    context = {
        'user_bmi': user_bmi,
        'activity_programs': activity_programs,
        'diet_plans': diet_plans,
        'activity_form': activity_form,
        'weekly_calories': weekly_calories,
        'calories_goal_progress': calories_goal_progress,
        'user_goal': user_goal * 7,
        'monthly_report': monthly_report,
    }

    return render(request, 'dashboard.html', context)

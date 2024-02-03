from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    age = models.IntegerField(default=18)
    height = models.FloatField(default=160)
    weight = models.FloatField(default=50)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    bmi = models.FloatField(default=0)
    daily_calories_burn_goal = models.FloatField(default=0)


class ActivityType(models.Model):
    name = models.CharField(max_length=100)
    unit_duration_minutes = models.PositiveIntegerField()
    calories_burn = models.FloatField()

    def __str__(self):
        return self.name


class Activity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    date = models.DateField()
    activity_type = models.ForeignKey(ActivityType, on_delete=models.CASCADE)
    duration_minutes = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.name} - {self.activity_type.name} - {self.date} - {self.duration_minutes}"

class ActivityProgram(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image_name = models.CharField(max_length=255)
    bmi_from = models.FloatField()
    bmi_to = models.FloatField()

    def __str__(self):
        return self.name


class DietPlan(models.Model):
    name = models.CharField(max_length=100)
    image_name = models.CharField(max_length=255)
    preparation_time = models.CharField(max_length=50)
    carbohydrate = models.FloatField()
    protein = models.FloatField()
    fat = models.FloatField()
    energy = models.FloatField()
    ingredients = models.TextField()
    guide = models.TextField()
    bmi_from = models.FloatField()
    bmi_to = models.FloatField()

    def __str__(self):
        return self.name

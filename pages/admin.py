from django.contrib import admin
from .models import ActivityType, ActivityProgram, DietPlan

admin.site.register(ActivityType)
admin.site.register(ActivityProgram)
admin.site.register(DietPlan)
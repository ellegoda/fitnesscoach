from allauth.account.forms import SignupForm
from django import forms
from .models import CustomUser, Activity


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['date', 'activity_type', 'duration_minutes']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker'}),
        }

    def __init__(self, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    age = forms.IntegerField(label='Age')
    height = forms.FloatField(label='Height')
    weight = forms.FloatField(label='Weight')
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female')], label='Gender')
    daily_calories_burn_goal = forms.IntegerField(label='Daily Calories Burn Goal')

    def save(self, request):
        user = super().save(request)
        user.age = self.cleaned_data['age']
        user.height = self.cleaned_data['height']
        user.weight = self.cleaned_data['weight']
        user.gender = self.cleaned_data['gender']
        user.daily_calories_burn_goal = self.cleaned_data['daily_calories_burn_goal']
        user.bmi = round(user.weight / ((user.height / 100) ** 2), 2)
        user.save()
        return user

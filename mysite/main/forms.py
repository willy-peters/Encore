from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Vote
from django.forms.widgets import NumberInput

# Forms creation

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required = True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit = True):
        user = super(NewUserForm, self).save(commit = False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    

# User form
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name','last_name','email')

# Profile form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('product',)


# Vote form
class VoteForm(forms.ModelForm):

    # Overriding the input fields with Bootstrap styling
    comfort = forms.IntegerField(widget = NumberInput(attrs = {'placeholder': '(5)', 'type': 'range', 'min': '1', 'max': '10', 'class': 'form-range comfort', 'value': '5'}))
    performance = forms.IntegerField(widget = NumberInput(attrs = {'placeholder': '(5)', 'type': 'range', 'min': '1', 'max': '10', 'class': 'form-range performance', 'value': '5'}))
    durability = forms.IntegerField(widget = NumberInput(attrs = {'placeholder': '(5)', 'type': 'range', 'min': '1', 'max': '10', 'class': 'form-range durability', 'value': '5'}))

    class Meta:
        model = Vote
        fields = ('comfort', 'performance', 'durability')


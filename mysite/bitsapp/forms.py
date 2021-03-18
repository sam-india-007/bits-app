from django import forms
from .models import Question, Answers, Profile
from django.contrib.auth.models import User



class answerForm(forms.ModelForm):
    ans = forms.Textarea
    class Meta:
        model=Answers
        
        fields=['ans']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        
class ProfileUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['dp']
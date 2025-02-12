from django import forms
from .models import Project, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProjectForm(forms.ModelForm):
     class Meta:
          model = Project
          fields = ['text', 'image']

class UserRegistrationForm(UserCreationForm):
     email = forms.EmailField()
     class Meta:
          model = User
          fields = ('username', 'email', 'password1', 'password2')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'rating']
        widgets = {
            'rating': forms.HiddenInput(),
        }
    
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if not 1 <= rating <= 5:
            raise forms.ValidationError("Rating must be between 1 and 5")
        return rating


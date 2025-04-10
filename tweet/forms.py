from django import forms
from .models import Project, Comment, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProjectForm(forms.ModelForm):
     class Meta:
          model = Project
          fields = ['name','text', 'image','project_type']
          labels={
              'name':'Project name',
              'text':'Description',
              'project_type':'Select Project Category'
          }
          widgets={
              'project_type':forms.RadioSelect(attrs={
                  'class':'hidden peer'
              })
          }

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

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'background_picture', 'linkedin_url']

        widgets = {
            'linkedin_url': forms.URLInput(attrs={'class': 'w-full p-2 border rounded-lg'})
        }

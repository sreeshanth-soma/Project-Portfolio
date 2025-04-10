from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


PROJECT_TYPE_CHOICES = [
    ('Personal Project', 'Personal Project'),
    ('Real-Time Project', 'Real-Time Project'),
    ('Minor Project', 'Minor Project'),
    ('Major Project', 'Major Project'),
    ('Research Project', 'Research Project'),
    ('Coursework Project', 'Coursework Project'),
]

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False, null=False, default="")
    text = models.TextField()
    image = models.ImageField(upload_to='photos/', blank=True, null=True)
    project_type = models.CharField(max_length=50, choices=PROJECT_TYPE_CHOICES, default='Personal Project')  # ← NEW FIELD
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def average_rating(self):
        avg_rating = self.comments.aggregate(avg_rating=Avg('rating'))['avg_rating']
        return round(avg_rating, 1) if avg_rating is not None else 0  # Round to 1 decimal place

    def __str__(self):
        return f'{self.user.username} - {self.name}'  # Modified here

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=500)
    rating = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'project')  # Ensures one comment per user per project

    def __str__(self):
        return f'{self.user.username} - {self.project.text}'
    
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    background_picture = models.ImageField(upload_to='background_pics/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    linkedin_url = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'
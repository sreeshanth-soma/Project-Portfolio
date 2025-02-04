from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=240)
    image = models.ImageField(upload_to='photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def average_rating(self):
        avg_rating = self.comments.aggregate(avg_rating=Avg('rating'))['avg_rating']
        return round(avg_rating, 1) if avg_rating is not None else 0  # Round to 1 decimal place

    def __str__(self):
        return f'{self.user.username} - {self.text[:30]}'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=500)
    rating = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project')  # Ensures one comment per user per project

    def __str__(self):
        return f'{self.user.username} - {self.project.text}'

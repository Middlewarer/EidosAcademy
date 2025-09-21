from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    user = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=255)
    text = models.TextField(blank=True, null=True)
    grade = models.DecimalField(max_digits=3, decimal_places=2)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='reviews')

class Category(models.Model):
    title = models.CharField(max_length=100)

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='courses', null=True, blank=True)


    def __str__(self):
        return self.title

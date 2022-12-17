from django.db import models
from django.db.models import Count
from django.contrib.auth import get_user_model

from datetime import datetime
import uuid

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to="profile_images", default="default-avatar.png")
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to="post_images")
    caption = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # https://docs.djangoproject.com/en/4.1/ref/models/fields/#django.db.models.DateField.auto_now_add
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user


class Contact(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    message = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return f"{self.id} - {self.surname} - {self.email}"
from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar=models.ImageField(upload_to='media/profile.avatar', default='media/profile.avatar/111111.jpg')


class Post(models.Model):
    text=models.TextField()
    photo = models.ImageField(upload_to='media/post')
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name='following')
    followers = models.ManyToManyField(User, related_name='followers')



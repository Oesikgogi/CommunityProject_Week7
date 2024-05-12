from django.db import models
from accounts.models import CustomUser

class Post(models.Model):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
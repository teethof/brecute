
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted2 = models.TimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk':self.pk})

    @property
    def comments_num(self):
        return PostComment.objects.filter(post=self).count()

class PostComment(models.Model):
    post_connected = models.ForeignKey(Post, related_name='comments', on_delete=CASCADE)
    author = models.ForeignKey(User, related_name='author', on_delete=CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return str(self.author)+', '+self.post_connected.title[:40]
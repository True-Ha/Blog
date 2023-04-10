from django.conf import settings
from django.db import models
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        )
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('Post_detail', args=[str(self.id)])

class Comment(models.Model):
    Post = models.ForeignKey(Post,
                                on_delete=models.CASCADE,
                                related_name='comments')
    comment = models.CharField(max_length=140)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.comment
    
    def get_absolute_url(self):
        return reverse('posts/Post_list')
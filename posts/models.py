from django.conf import settings
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager

class IpModel(models.Model):
     ip = models.CharField(max_length=100)

     def __str__(self):
          return self.ip

class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    views = models.ManyToManyField(IpModel, related_name="post_views", blank=True)
    likes = models.ManyToManyField(IpModel, related_name="post_likes", blank=True)
    banner = models.ImageField("Banner", upload_to="posts/", null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        )
    
    slug = models.SlugField(max_length=130, unique=True, null=True, db_index=True, verbose_name="URL")
    draft = models.BooleanField("Черновик", default=False)
    tags = TaggableManager()

    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('Post_detail', kwargs={"slug": self.slug})
    
    def total_views(self): 
        return self.views.count()
    
    def total_likes(self): 
        return self.likes.count()
    
    
# args=[str(self.id)]  kwargs={"slug": self.url}


class Comment(models.Model):
    post = models.ForeignKey(Post,
                                on_delete=models.CASCADE,
                                related_name='comments')
    comment = models.TextField(max_length=140)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True,
        related_name='patents'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
            return '%s - %s' % (self.post.title, self.author)

    


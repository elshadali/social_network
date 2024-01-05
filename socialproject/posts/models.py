from django.db import models
from django.conf import settings
from django.utils.text import slugify



class Posts(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    body = models.TextField(blank=True)
    image = models.ImageField(upload_to='posts/%y/%m/%d')
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=250, blank=True)
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='posts_liked', blank=True)


    def __str__(self):
        return self.title
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments')
    body = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now=True)
    posted_by = models.CharField(max_length=100)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.body
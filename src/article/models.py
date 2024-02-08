from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from taggit.managers import TaggableManager


class Post(models.Model):

    title = models.CharField(max_length=255, unique=True,  blank=True, null=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    img = models.ImageField(upload_to="articles/images")
    in_trend = models.BooleanField(default=False, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    request_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name='category')

    tags = TaggableManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title if self.title else "No title"

    def get_absolute_url(self):
        return reverse('article:detail_post', args=[str(self.slug)])

    class Meta:
        verbose_name = "article"
        verbose_name_plural = "articles"
        ordering = ['-created_at']


class Category(models.Model):

    title = models.CharField(max_length=255, unique=True, blank=True, null=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title if self.title else "No title"

    def get_absolute_url(self):
        return reverse('article:category_detail', args=[str(self.slug)])

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"


class FriendlyLink(models.Model):
    friend = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, unique=True, blank=True, null=True)
    link = models.URLField(max_length=128, db_index=True, unique=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('article:friend_detail', args=[str(self.friend), str(self.name), str(self.link)])

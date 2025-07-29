from django.db import models
from django.conf import settings
from bs4 import BeautifulSoup
from django.conf import settings
import os
 

class Article(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=255)  # Matches `newArticle.title`
    excerpt = models.TextField(blank=True, null=True)  # Matches `newArticle.excerpt`
    category = models.CharField(max_length=100)  # Matches `newArticle.category`
    image_url = models.ImageField(upload_to='uploads/', blank=True, null=True)  # Matches `newArticle.imageUrl`
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='articles'
    ) # Link to Author model
    #author = models.TextField(blank=False, null=False, default='Fred')
    content = models.TextField(blank=True, null=True)  # Matches `newArticle.content`
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')  # Matches `newArticle.status`
    is_auto_update = models.BooleanField(default=False)  # Matches `newArticle.is_auto_update`
    published_date = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    created_at = models.DateTimeField(auto_now_add=True)  # Optional: Matches `created_at`
    last_updated = models.DateTimeField(auto_now=True)  # Optional: Matches `last_updated`
    tags = models.JSONField(blank=True, null=True)  # Optional: Matches `tags`
    is_featured = models.BooleanField(default=False)  # For featured articles
    is_editors_pick = models.BooleanField(default=False) 
    views = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.image_url and self.content:
            soup = BeautifulSoup(self.content, 'html.parser')
            img_tag = soup.find('img')
            if img_tag and img_tag.get('src'):
                relative_path = img_tag['src']
                # Ensure the path is absolute
                if relative_path.startswith('/media/'):
                    self.image_url = f"{settings.SITE_URL}{relative_path}"   # Build absolute URL
                elif not relative_path.startswith('http'):
                    self.image_url = os.path.join(settings.MEDIA_URL, relative_path.lstrip('/'))
                else:
                    self.image_url = relative_path
                print(f"Extracted image_url: {self.image_url}")  # Debugging
        super().save(*args, **kwargs)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Matches `newCategory.name`
    slug = models.SlugField(max_length=100, unique=True)  # Matches `newCategory.slug`
    count = models.PositiveIntegerField(default=0)  # Optional: Tracks the number of articles in this category
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation

    def __str__(self):
        return self.name


    




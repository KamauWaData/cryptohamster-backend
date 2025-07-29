from django.contrib import admin
from django.contrib import admin
from .models import Article, Category

# Register the CustomUser model
admin.site.register(Article)
admin.site.register (Category)


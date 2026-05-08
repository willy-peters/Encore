from django.contrib import admin
from .models import Product, Article, Tag

# Register your models here.

# Product Model
admin.site.register(Product)

# Article Model
admin.site.register(Article)

# Tag model
admin.site.register(Tag)
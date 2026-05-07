from django.db import models
from tinymce import HTMLField   

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=150)
    product_type = models.CharField(max_length=25)    
    product_description = models.TextField()
    affliate_url = models.SlugField(blank=True, null=True)
    product_image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.product_name
    

# Article model
class Article(models.Model):
    article_title = models.CharField(max_length=200)
    article_published = models.DateField('date published')
    article_content = HTMLField()
    article_image = models.ImageField(upload_to='images/')
    article_slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.article_title
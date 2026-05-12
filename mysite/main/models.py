from django.db import models
from tinymce import HTMLField   
from django.contrib.auth.models import User
from django.dispatch import receiver 
from django.db.models.signals import post_save

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=150)
    product_type = models.CharField(max_length=25)    
    product_description = models.TextField()
    affliate_url = models.SlugField(blank=True, null=True)
    product_image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.product_name
    

# Tag model => to create label articles and create categories in nav bar
class Tag(models.Model):
    tag_name = models.CharField(max_length=15)
    tag_slug = models.SlugField()

    def __str__(self):
        return self.tag_name




# Article model
class Article(models.Model):
    article_title = models.CharField(max_length=200)
    article_published = models.DateField('date published')
    article_content = HTMLField()
    article_image = models.ImageField(upload_to='images/')
    article_slug = models.SlugField(blank=True, null=True)
    article_tags = models.ManyToManyField(Tag) # creates a dropdown in Article pages in admin allowing tag creation

    def __str__(self):
        return self.article_title
    

# Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)

    # decorator functions to override create_user_profile and save_user_profile functions from User model
    @receiver(post_save, sender = User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user = instance)

    @receiver(post_save, sender = User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


# Vote model (voting the quality of products)
class Vote(models.Model):
    profile = models.ForeignKey(Profile, on_delete = models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    comfort = models.IntegerField(default=0)
    performance = models.IntegerField(default=0)
    durability = models.IntegerField(default=0)



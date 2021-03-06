from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from datetime import datetime
from ckeditor.fields import RichTextField


# Create your models here.

class Category(models.Model): 
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique = True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self): return self.name

class Tag(models.Model):
    name = models.CharField(max_length=10, unique=True)
    def __str__(self): return self.name

class Photo(models.Model):
    TITLE_MAX_LENGTH=128
    DESCRIPTION_MAX_LENGTH=500
    
    Image = models.ImageField(upload_to='upload_photos', blank=False, null= False)
    Description = models.TextField(max_length=DESCRIPTION_MAX_LENGTH, null=True)
    Like = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    Tag = models.ManyToManyField(Tag)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, blank=False)
    Date = models.DateField(default=datetime.now)
    Title = models.CharField(max_length=TITLE_MAX_LENGTH, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self): return self.Title
    
class UserProfile(models.Model):
    #link UserProfile to a User model instance
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    NICKNAME_MAX_LENGTH=20
    DESCRIPTION_MAX_LENGTH=500
    POSTCODE_MAX_LENGTH=10

    nickname = models.CharField(max_length=NICKNAME_MAX_LENGTH, null=False)
    gender = models.CharField(max_length=10, null=False)
    description = models.TextField(max_length=DESCRIPTION_MAX_LENGTH, null=False)
    postcode = models.CharField(max_length=POSTCODE_MAX_LENGTH, null=False)
    favorite = models.ManyToManyField(Photo, related_name="user_favoirte")
    # review = models.ManyToManyField(Review, related_name="user_review")
    following = models.ManyToManyField(User, related_name="user_following")
    # photo = models.ForeignKey(Photo, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='profile_images', blank=False)

    def __str__(self): return self.user.username

class Review(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=False, blank=False)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0)
    content = RichTextField(max_length=1000, null=False)

    def __str__(self): return self.content

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    question = models.TextField(max_length=1000, null=False)
    date = models.DateField(default=datetime.now)

    def __str__(self): return self.user.username
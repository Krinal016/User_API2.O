from django.db import models
from django.utils.text import slugify
# Create your models here.

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = "email" 
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def is_authenticated(self):
        return True  

    @property
    def is_anonymous(self):
        return False  

class Blog(models.Model):
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    slug = models.SlugField(unique=True, null=False, blank=True)
    author = models.ForeignKey(Users, on_delete=models.CASCADE) 
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
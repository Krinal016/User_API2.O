from django.db import models

# Create your models here.

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)  # Required
    is_staff = models.BooleanField(default=False)  # Required
    is_superuser = models.BooleanField(default=False) 
    
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
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Blog,Users
from django.conf import settings
from django.core.mail import send_mail


@receiver(pre_save, sender=Blog)
def create_slug(sender, instance, **kwargs):
    """Automatically generate a unique slug before saving"""
    if not instance.slug:
        base_slug = slugify(instance.title)
        slug = base_slug
        count = 1

        while Blog.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{count}"
            count += 1

        instance.slug = slug

# @receiver(post_save, sender=Users)
# def send_welcome_email(sender, instance, created, **kwargs):
#     if created and instance.email:
#         subject = 'Welcome to Our Website'
#         message = f'Hello {instance.email},\n\nWelcome to our website! Thank you for joining us.'
#         from_email = settings.EMAIL_HOST_USER
#         recipient_list = [instance.email]
#         send_mail(subject, message, from_email, recipient_list)
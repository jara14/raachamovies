from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Movie(models.Model):
    CATEGORY_CHOICES = (
        ('now_showing', 'Now Showing'),
        ('upcoming', 'Upcoming'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    poster = models.ImageField(upload_to='posters/')
    video_file = models.FileField(upload_to='movies/', blank=True, null=True)

    price = models.PositiveIntegerField(default=100)
    show_date = models.DateField(blank=True, null=True)
    show_time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='now_showing')

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Change this from OneToOneField to ForeignKey
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Booking(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Added this
    name = models.CharField(max_length=100)
    email = models.EmailField()
    tickets = models.PositiveIntegerField()
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.movie.title}"


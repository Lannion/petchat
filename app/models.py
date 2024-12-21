from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.user.username}: {self.content[:20]}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Store images in 'profile_pics/' folder
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

class MissingPetReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="missing_pet_reports")
    pet_name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField()
    last_seen = models.CharField(max_length=255)
    date_last_seen = models.DateField()
    contact_info = models.CharField(max_length=255)
    pet_picture = models.ImageField(upload_to="missing_pets/")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pet_name} (Reported by {self.user.username})"

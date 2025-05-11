from django.db import models

from apps.users.models import User


class Kid(models.Model):
    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"

    full_name = models.CharField(max_length=128)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=6, choices=Gender.choices)
    photo = models.ImageField(upload_to="media/", blank=True, null=True)
    bio = models.TextField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="kids")

    class Meta:
        ordering = ["-date_of_birth"]

    def __str__(self):
        return self.full_name

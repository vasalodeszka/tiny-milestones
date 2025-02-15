from django.db import models

from apps.users.models import User


class Kid(models.Model):
    GENDER_CHOICES = [("male", "Male"), ("female", "Female")]

    family_name = models.CharField(max_length=64)
    given_name = models.CharField(max_length=64)
    birth_date = models.DateField()
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    photo = models.ImageField(upload_to="media/", blank=True, null=True)
    bio = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="kids")

    class Meta:
        verbose_name = "Kid"
        verbose_name_plural = "Kids"

    def __str__(self):
        return f"{self.family_name} {self.given_name}"

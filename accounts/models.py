from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    about = models.TextField()
    avatar = models.ImageField()

    def __str__(self) -> str:
        return self.user.username

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"

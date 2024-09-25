from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4


def service_upload_to(instance, filename):
    return f"services/{instance.user.username}/{filename}"


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=service_upload_to)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"


class ServiceOrder(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Aberta"
        CANCELED = "CANCELED", "Cancelada"
        DONE = "DONE", "Finalizada"
        FINISHED = "FINISHED", "Concluída"

    code = models.UUIDField(default=uuid4, editable=False)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    extra_info = models.TextField()
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.OPEN
    )

    def __str__(self):
        return str(self.code)

    class Meta:
        verbose_name = "Oderm de Serviço"
        verbose_name_plural = "Ordens de Serviço"

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.service.user.email_user(
                subject="Nova ordem de serviço",
                message=f"Você tem uma nova ordem de serviço para o serviço {self.service.name}",
            )
        return super().save(args, kwargs)

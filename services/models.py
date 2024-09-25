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
    mean_rating = models.DecimalField(
        max_digits=3, decimal_places=2, default=0, editable=False
    )
    rating_count = models.PositiveIntegerField(default=0, editable=False)

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


class ServiceOrderReview(models.Model):
    service_order = models.ForeignKey(ServiceOrder, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"

    def __notify_user(self):
        self.service_order.service.user.email_user(
            subject="Nova avaliação",
            message=f"Você recebeu uma nova avaliação para o serviço {self.service_order.service.name}",
        )

    def __update_service_order_status(self):
        self.service_order.status = ServiceOrder.Status.FINISHED
        self.service_order.save()

    def __update_service_rating(self):
        service = self.service_order.service
        service.mean_rating = (
            (service.mean_rating * service.rating_count) + self.rating
        ) / (service.rating_count + 1)
        service.rating_count += 1
        service.save()

    def __update_profile_rating(self):
        profile = self.service_order.service.user.profile
        profile.mean_rating = (
            (profile.mean_rating * profile.rating_count) + self.rating
        ) / (profile.rating_count + 1)
        profile.rating_count += 1
        profile.save()

    def save(self, *args, **kwargs):
        self.__notify_user()

        self.__update_service_order_status()

        self.__update_service_rating()

        self.__update_profile_rating()

        return super().save(args, kwargs)

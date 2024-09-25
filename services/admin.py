from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

from .models import Service, ServiceOrder, ServiceOrderReview


@admin.register(ServiceOrderReview)
class ServiceOrderReviewAdmin(admin.ModelAdmin):
    list_display = (
        "service_order__service__name",
        "service_order__name",
        "service_order__email",
        "rating",
    )

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(service_order__service__user=request.user)


@admin.register(ServiceOrder)
class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "service",
        "name",
        "email",
        "phone",
        "status",
    )
    list_filter = ("service", "status")
    actions = ("cancel_service_order", "done_service_order")

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(service__user=request.user)

    @admin.action(description="Cancelar ordens de serviço")
    def cancel_service_order(self, request, queryset):
        queryset.filter(status=ServiceOrder.Status.OPEN).update(
            status=ServiceOrder.Status.CANCELED
        )
        self.message_user(request, "Ordens de serviço canceladas com sucesso")

    @admin.action(description="Finalizar ordens de serviço")
    def done_service_order(self, request, queryset):
        queryset.filter(status=ServiceOrder.Status.OPEN).update(
            status=ServiceOrder.Status.DONE
        )

        for service_order in queryset:
            relative_review_url = reverse(
                "services:create_review", kwargs={"code": service_order.code}
            )
            absolute_review_url = request.build_absolute_uri(relative_review_url)

            message = f"Olá {service_order.name},\n\n"
            message += f"Sua ordem de serviço {service_order.code} foi finalizada.\n\n"
            message += f"Serviço: {service_order.service.name}\n"
            message += f"Preço: R$ {service_order.service.price:.2f}\n\n"
            message += f"Avalie o serviço em: {absolute_review_url}\n\n"
            message += "Atenciosamente,\n"
            message += "Equipe TWNinjas"

            send_mail(
                "Odem de serviço finalizada",
                message,
                settings.CONTACT_EMAIL,
                [service_order.email],
            )

        self.message_user(request, "Ordens de serviço finalizadas com sucesso")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "user", "mean_rating", "rating_count")
    list_filter = ("user",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.user = request.user
        return super().save_model(request, obj, form, change)

    def get_exclude(self, request, obj):
        if not request.user.is_superuser and not obj:
            return ["user"]
        return []

    def get_readonly_fields(self, request, obj):
        if obj and not request.user.is_superuser:
            return ["user"]
        return []

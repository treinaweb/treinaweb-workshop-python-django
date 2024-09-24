from django.contrib import admin

from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "user")
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

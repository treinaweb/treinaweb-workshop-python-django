from django import forms

from .models import ServiceOrder


class ServiceOrderForm(forms.ModelForm):
    class Meta:
        model = ServiceOrder
        fields = (
            "service",
            "name",
            "email",
            "phone",
            "address",
            "extra_info",
        )
        widgets = {
            "address": forms.TextInput(),
            "service": forms.HiddenInput(),
        }

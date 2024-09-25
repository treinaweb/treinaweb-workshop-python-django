from django import forms

from .models import ServiceOrder, ServiceOrderReview


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


class ServiceOrderReviewForm(forms.ModelForm):
    class Meta:
        model = ServiceOrderReview
        fields = ("rating", "comment", "service_order")
        widgets = {
            "service_order": forms.HiddenInput(),
            "rating": forms.HiddenInput(attrs={"id": "rating-value"}),
            "comment": forms.Textarea(
                attrs={
                    "id": "review-text",
                    "placeholder": "Deixe seu depoimento...",
                    "rows": 19,
                }
            ),
        }

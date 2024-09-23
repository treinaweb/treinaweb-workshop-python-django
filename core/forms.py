from django import forms
from django.core.mail import send_mail
from django.conf import settings


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"placeholder": "Digite seu nome"})
    )
    email = forms.EmailField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Digite seu e-mail"}),
    )
    phone = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Digite seu número"}),
    )
    address = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "Digite seu endereço"}),
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder": "Deixe a sua mensagem para os nossos ninjas"}
        )
    )

    def send_mail(self):
        name = self.cleaned_data["name"]
        email = self.cleaned_data["email"]
        phone = self.cleaned_data["phone"]
        address = self.cleaned_data["address"]
        message = self.cleaned_data["message"]

        send_mail(
            f"Messagem de {name} <{email}>",
            f"Telefone: {phone}\nEndereço: {address}\n\nMensagem: {message}",
            email,
            [settings.CONTACT_EMAIL],
        )

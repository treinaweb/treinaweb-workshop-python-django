from django.shortcuts import render

from services.models import Service
from .forms import ContactForm


def home(request):
    cities = (
        Service.objects.filter(user__profile__isnull=False)
        .values("user__profile__city")
        .distinct()
    )
    cities = [city["user__profile__city"] for city in cities]
    return render(request, "core/home.html", {"cities": cities})


def about(request):
    return render(request, "core/about.html")


def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.send_mail()
        form = ContactForm()
    return render(request, "core/contact.html", {"form": form})

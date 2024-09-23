from django.shortcuts import render

from .forms import ContactForm


def home(request):
    return render(request, "core/home.html")


def about(request):
    return render(request, "core/about.html")


def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.send_mail()
        form = ContactForm()
    return render(request, "core/contact.html", {"form": form})

from django.shortcuts import render

from .models import Service


def list(request):
    services = Service.objects.all()
    return render(request, "services/list.html", {"services": services})

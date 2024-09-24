from django.shortcuts import render
from django.core.paginator import Paginator
from django.conf import settings

from .models import Service


def list(request):
    services = Service.objects.all()
    paginator = Paginator(services, settings.PAGE_SIZE)

    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    return render(request, "services/list.html", {"page_obj": page_obj})

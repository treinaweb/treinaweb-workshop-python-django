from django.shortcuts import render
from django.core.paginator import Paginator
from django.conf import settings

from .models import Service


def list(request):
    q = request.GET.get("q", "")
    city = request.GET.get("city")

    services = Service.objects.filter(name__icontains=q)
    if city:
        services = services.filter(user__profile__city=city)
    paginator = Paginator(services, settings.PAGE_SIZE)

    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    cities = (
        Service.objects.filter(user__profile__isnull=False)
        .values("user__profile__city")
        .distinct()
    )
    cities = [city["user__profile__city"] for city in cities]
    return render(
        request, "services/list.html", {"page_obj": page_obj, "cities": cities}
    )

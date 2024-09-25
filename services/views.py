from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.conf import settings

from .models import Service
from .forms import ServiceOrderForm


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


def detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, "services/detail.html", {"service": service})


def create_order(request, pk):
    service = get_object_or_404(Service, pk=pk)
    form = ServiceOrderForm(request.POST or None, initial={"service": service})
    if form.is_valid():
        form.save()
        return redirect("services:detail", pk=pk)
    return render(
        request, "services/create_order.html", {"service": service, "form": form}
    )

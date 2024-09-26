from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.conf import settings

from .models import Service, ServiceOrder, ServiceOrderReview
from .forms import ServiceOrderForm, ServiceOrderReviewForm
from .utils import calculate_approval_rate, calculate_conclusion_rate


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
    reviews = ServiceOrderReview.objects.filter(service_order__service=service)
    done_services = ServiceOrder.objects.filter(
        service=service,
        status__in=[ServiceOrder.Status.DONE, ServiceOrder.Status.FINISHED],
    ).count()
    user_done_services = ServiceOrder.objects.filter(
        service__user=service.user,
        status__in=[ServiceOrder.Status.DONE, ServiceOrder.Status.FINISHED],
    ).count()
    approval_rate = calculate_approval_rate(reviews)
    conclusion_rate = calculate_conclusion_rate(service, user_done_services)
    return render(
        request,
        "services/detail.html",
        {
            "service": service,
            "reviews": reviews,
            "done_services": done_services,
            "user_done_services": user_done_services,
            "approval_rate": approval_rate,
            "conclusion_rate": conclusion_rate,
        },
    )


def create_order(request, pk):
    service = get_object_or_404(Service, pk=pk)
    form = ServiceOrderForm(request.POST or None, initial={"service": service})
    if form.is_valid():
        form.save()
        return redirect("services:detail", pk=pk)
    return render(
        request, "services/create_order.html", {"service": service, "form": form}
    )


def create_review(request, code):
    service_order = get_object_or_404(ServiceOrder, code=code)
    form = ServiceOrderReviewForm(
        request.POST or None, initial={"service_order": service_order}
    )
    if service_order.status != ServiceOrder.Status.DONE:
        return redirect("services:detail", pk=service_order.service.pk)
    if form.is_valid():
        form.save()
        return redirect("services:detail", pk=service_order.service.pk)
    return render(
        request,
        "services/create_review.html",
        {"service_order": service_order, "form": form},
    )

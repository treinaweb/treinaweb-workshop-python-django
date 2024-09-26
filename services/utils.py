from .models import ServiceOrder


def calculate_approval_rate(reviews):
    if reviews.count():
        return (reviews.filter(rating__gte=3).count() / reviews.count()) * 100
    return 0


def calculate_conclusion_rate(service, user_done_services):
    user_service_orders_count = ServiceOrder.objects.filter(
        service__user=service.user
    ).count()

    if user_service_orders_count:
        return (user_done_services / user_service_orders_count) * 100
    return 0

from django.shortcuts import render, redirect

from .forms import RegisterForm
from .models import UserProfile


def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.is_staff = True
        user.save()
        UserProfile.objects.create(user=user)
        return redirect("admin:login")
    return render(request, "accounts/register.html", {"form": form})

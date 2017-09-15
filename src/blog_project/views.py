from django.shortcuts import render


def home(request):
    context = {}
    return render(request, "index1.html", context)

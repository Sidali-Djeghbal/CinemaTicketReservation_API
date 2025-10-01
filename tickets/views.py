from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def no_restFramework_method(request):
    guests = [
        {'id': 1, 'name': 'Ali'},
        {'id': 2, 'name': 'Ahmed'},
    ]
    return JsonResponse(guests, safe=False)
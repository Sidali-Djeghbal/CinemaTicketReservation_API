from django.shortcuts import render
from django.http import JsonResponse
from tickets.models import Guest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import GuestSerializer
# Create your views here.

# no REST framework method
def no_rest_no_model(request):
    guests = [
        {'id': 1, 'name': 'Ali'},
        {'id': 2, 'name': 'Ahmed'},
    ]
    return JsonResponse(guests, safe=False)

# model data default method without REST framework
def no_rest_from_model(request):
    data = Guest.objects.all()
    response = {
        'guests': list(data.values('name', 'mobile'))
    }
    return JsonResponse(response)

# model data method with REST framework
# GET , POST
@api_view(['GET', 'POST'])
def FBV_list(request):
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

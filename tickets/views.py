from django.shortcuts import render
from django.http import JsonResponse
from tickets.models import Guest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, filters
from .serializers import GuestSerializer
# Create your views here.

# no REST framework method
def no_rest_no_model(request):
    guests = [
        {'id': 1, 'name': 'Ali'},
        {'id': 2, 'name': 'Ahmed'},
    ]
    return JsonResponse(guests, safe=False)

# data model default method without rest
def no_rest_from_model(request):
    data = Guest.objects.all()
    response = {
        'guests': list(data.values('id','name'))
    }
    return JsonResponse(response)

# data model method with REST framework
#function based views (GET, POST)
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
            return Response(serializer.data, 
                            status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
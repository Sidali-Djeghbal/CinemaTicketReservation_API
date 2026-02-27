from django.shortcuts import render
from django.http import JsonResponse
from tickets.models import Guest, Movie, Reservation
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics, mixins, viewsets, filters
from .serializers import GuestSerializer, MovieSerializer, ReservationSerializer
from rest_framework.views import APIView
from django.http import Http404
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
    

@api_view(['GET', 'PUT', 'DELETE'])
def FBV_pk(request, pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#class based views

class CBV_List(APIView):
    def get(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.data,
            status=status.HTTP_400_BAD_REQUEST
        )
        
        
class CBV_pk(APIView):
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404
    def get(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    def put(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# mixins and generics method
class mixins_list(mixins.ListModelMixin, mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    def get(self, request):
        return self.list(request)
    def post(self, request):
        return self.create(request)
    
class mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    def get(self, request,pk):
        return self.retrieve(request)
    def put(self, request,pk):
        return self.update(request)
    def delete(self, request,pk):
        return self.destroy(request)
    
class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    
class generic_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    
class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    
class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['movie']

class viewsets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
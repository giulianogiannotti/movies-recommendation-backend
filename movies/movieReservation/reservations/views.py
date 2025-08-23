from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Reservation, Seat, ReservationSeat, Function, Auditorium, Movie, User
from .serializers import (ReservationSerializer, SeatSerializer, ReservationSeatSerializer,
                          FunctionSerializer, AuditoriumSerializer, MovieSerializer, UserSerializer)



class ReservationListCreateView(APIView):
    """
    View to list all reservations of the user or create a new reservation.
    """
    def get(self, request):
        testUser = User.objects.first()
        reservations = Reservation.objects.filter(user=testUser)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    def post(self, request):
        testUser = User.objects.first()
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=testUser)  # Assuming the user is authenticated
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
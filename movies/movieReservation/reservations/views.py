from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Reservation, Seat, ReservationSeat, Function, Auditorium, Movie, User
from .serializers import (ReservationSerializer, SeatSerializer, ReservationSeatSerializer,
                          FunctionSerializer, AuditoriumSerializer, MovieSerializer, UserSerializer)
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


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



class LoginOrRegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Faltan credenciales"}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Intentar autenticar
        user = authenticate(username=username, password=password)
        if user:
            token = self.get_tokens_for_user(user)
            return Response({"msg": "Login exitoso", "token": token})

        # 2. Si no existe, registrar
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            token = self.get_tokens_for_user(user)
            return Response({"msg": "Usuario creado", "token": token}, status=status.HTTP_201_CREATED)

        return Response({"error": "Credenciales incorrectas"}, status=status.HTTP_401_UNAUTHORIZED)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
from rest_framework import serializers
from .models import Reservation, Seat, ReservationSeat, Function, Auditorium, Movie, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']       

class ReservationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Reservation
        fields = ['id', 'user', 'function', 'reservation_date']   

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'seat_number', 'auditorium']                    

class ReservationSeatSerializer(serializers.ModelSerializer):
    reservation = ReservationSerializer(read_only=True)
    seat = SeatSerializer(read_only=True)
    
    class Meta:
        model = ReservationSeat
        fields = ['id', 'reservation', 'seat', 'function']  

class FunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Function
        fields = ['id', 'name', 'date_time', 'movie', 'auditorium', 'price']    

class AuditoriumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditorium
        fields = ['id', 'capacity'] 

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'name', 'genre', 'duration', 'rating']  


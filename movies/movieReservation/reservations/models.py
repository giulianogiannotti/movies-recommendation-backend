from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('regular', 'Regular'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='regular')

    def __str__(self):
        return f"{self.username} ({self.role})"



class Reservation(models.Model):
    """
    A brief description of what this model represents.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="The user who made the reservation.")
    function = models.ForeignKey('Function', on_delete=models.CASCADE, related_name='reservations', help_text="The function associated with the reservation.")
    movie_name = models.CharField(max_length=100, help_text="The name of the movie reserved.")
    reservation_date = models.DateTimeField(auto_now_add=True, help_text="The date and time when the reservation was made.")

    def __str__(self):          
        return f"Reservation {self.id} by {self.user.username} for {self.movie_name} on {self.function.date_time}"

class Seat(models.Model):
    """
    A brief description of what this model represents.
    """
    seat_number = models.CharField(max_length=10, unique=True, help_text="The unique identifier for the seat.")
    auditorium = models.ForeignKey('Auditorium', on_delete=models.CASCADE, related_name='seats', help_text="The auditorium where the seat is located.")

    def __str__(self):
        return f"Seat {self.seat_number} in Auditorium {self.auditorium.id}"

class ReservationSeat(models.Model):
    """
    A brief description of what this model represents.
    """
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='reservation_seats', help_text="The reservation associated with the seat.")
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='reservation_seats', help_text="The seat that is reserved.")
    function = models.ForeignKey('Function', on_delete=models.CASCADE, related_name='reservation_seats', help_text="The function during which the seat is reserved.")

    def __str__(self):
        return f"Seat {self.seat.seat_number} for Reservation {self.reservation.id}"    

class Function(models.Model):
    """A brief description of what this model represents.
    """
    name = models.CharField(max_length=100, help_text="The name of the function.")
    date_time = models.DateTimeField(help_text="The date and time when the function takes place.")
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='functions', help_text="The movie being shown in the function.")
    auditorium = models.ForeignKey('Auditorium', on_delete=models.CASCADE, related_name='functions', help_text="The auditorium where the function is held.")
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0, help_text="The price of the ticket for the function.")
  
    def available_seats(self):
        total_reserved = self.reservation_seats.count()  # cuantos asientos fueron reservados en esta función
        return self.auditorium.capacity - total_reserved

    def revenue(self):
        return self.reservation_seats.count() * self.price

    def __str__(self):
        return f"Function {self.name} for {self.movie.name} on {self.date_time} in Auditorium {self.auditorium.id}"

class Auditorium(models.Model):             
    """A brief description of what this model represents.
    """
    name = models.CharField(max_length=100, help_text="The name of the auditorium.")
    capacity = models.PositiveIntegerField(help_text="The seating capacity of the auditorium.")

    def __str__(self):
        return f"Auditorium {self.name} with capacity {self.capacity}"

class Movie(models.Model):
    """A brief description of what this model represents.
    """
    name = models.CharField(max_length=100, help_text="The name of the movie.")
    duration = models.PositiveIntegerField(help_text="The duration of the movie in minutes.")
    description = models.TextField(blank=True, help_text="A brief description of the movie.")
    poster_URL = models.URLField(blank=True, help_text="URL to the movie poster image.")    
    genre = models.CharField(max_length=50, blank=True, help_text="The genre of the movie.")

    def __str__(self):
        return f"Movie {self.name} ({self.duration} min)"


from django.contrib import admin
from .models import User, Movie, Auditorium, Function, Reservation, Seat, ReservationSeat


class FunctionAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_time', 'movie', 'auditorium', 'price')
    search_fields = ('name', 'movie__name', 'auditorium__name')
    list_filter = ('date_time', 'auditorium')
    readonly_fields = ('available_seats', 'revenue')


admin.site.register(User)
admin.site.register(Movie)
admin.site.register(Auditorium)
admin.site.register(Reservation)
admin.site.register(Seat)
admin.site.register(ReservationSeat)
admin.site.register(Function, FunctionAdmin)
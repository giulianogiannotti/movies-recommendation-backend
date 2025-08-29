from django.urls import path
from . import views

urlpatterns = [
    path('reservations/', views.ReservationListCreateView.as_view(), name='reservation-list'),
    path('auth/', views.LoginOrRegisterView.as_view(), name='login-or-register'),
]


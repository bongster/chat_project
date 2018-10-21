from django.contrib import admin
from django.urls import path

from .views import MessengersView, RoomsView

urlpatterns = [
    path('rooms/<int:pk>/', RoomsView.as_view()),
    path('', MessengersView.as_view()),
]

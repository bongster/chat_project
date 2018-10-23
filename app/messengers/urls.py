from django.urls import path

from .views import RoomDetailView, RoomView

urlpatterns = [
    path('rooms/<int:pk>', RoomDetailView.as_view()),
    path('rooms', RoomView.as_view()),
    path('', RoomView.as_view()),
]

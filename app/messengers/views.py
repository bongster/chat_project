import logging

from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView


# Create your views here.
from messengers.models import Message, Room, Room2User
from messengers.serializers import MessageSerializers

logger = logging.getLogger(__name__)


class RoomView(TemplateView):
    template_name = 'rooms/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['rooms'] = Room.objects.filter(
            pk__in=Room2User.objects.filter(
                user_id=self.request.user.id
            ).values_list('room_id', flat=True)
        )
        return context


class RoomDetailView(DetailView):
    template_name = 'rooms/detail.html'
    model = Room

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super().get_context_data(**kwargs)

        context['messages'] = MessageSerializers(Message.objects.filter(
            room_id=pk
        ),many=True).data

        context['pk'] = pk
        object = context['object']
        object.participated_users = get_user_model().objects.filter(
            pk__in=Room2User.objects.filter(
                room_id=pk,
            ).values_list('user_id', flat=True)
        )

        context['rooms'] = Room.objects.filter(
            pk__in=Room2User.objects.filter(
                user_id=self.request.user.id
            ).values_list('room_id', flat=True)
        )
        context['users'] = get_user_model().objects.exclude(
            pk__in=object.participated_users.values_list('pk', flat=True)
        )

        return context

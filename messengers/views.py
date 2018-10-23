import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView

# Create your views here.
from messengers.models import Message, Room, Room2User
from messengers.serializers import MessageSerializers, RoomSerializers

logger = logging.getLogger(__name__)


class SecureMixin(LoginRequiredMixin):
    login_url = '/login'
    redirect_field_name = 'redirect_to'


class RoomView(SecureMixin, TemplateView):
    template_name = 'rooms/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['rooms'] = RoomSerializers(Room.objects.filter(
            pk__in=Room2User.objects.filter(
                user_id=self.request.user.id
            ).values_list('room_id', flat=True)
        ), many=True, context={'request': self.request}).data

        return context


class RoomDetailView(SecureMixin, DetailView):
    template_name = 'rooms/detail.html'
    model = Room

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super().get_context_data(**kwargs)

        context['messages'] = MessageSerializers(
            Message.objects.filter(
                room_id=pk
            ), many=True
        ).data

        context['pk'] = pk
        object = context['object']
        object = RoomSerializers(instance=context['object'], context={'request', self.request}).data

        print(object)
        context['rooms'] = RoomSerializers(Room.objects.filter(
            pk__in=Room2User.objects.filter(
                user_id=self.request.user.id
            ).values_list('room_id', flat=True)
        ), many=True, context={'request': self.request}).data

        context['users'] = get_user_model().objects.exclude(
            pk__in=[ user['id'] for user in object['participated_users'] or [] ]
        )

        return context

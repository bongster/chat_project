from django.db.models import Q
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from .models import Room, Message, Room2User

# AttributeError: Manager isn't available; 'auth.User' has been swapped for 'users.user'
from django.contrib.auth import get_user_model

from django.contrib.auth.models import User


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RoomSerializers(serializers.ModelSerializer):
    participated_user = UserSerializers(required=False, many=True)

    class Meta:
        model = Room
        fields = '__all__'

    def create(self, validated_data):
        instance = super().create(validated_data)
        # TODO: instance 생성시에 Romm2User에 쌍으로 데이터 추가하기.
        Room2User.objects.create(
            room_id=instance.id,
            user_id=instance.owner_id,
        )

        Room2User.objects.create(
            room_id=instance.id,
            user_id=instance.owner_id,
        )

        return instance

    def to_representation(self, instance):
        users = get_user_model().objects.filter(
            pk__in=Room2User.objects.filter(
                Q(room_id=instance.id) & Q(user_id=self.context['request'].user.id)
            )
        )
        instance.participated_user = users
        return super().to_representation(instance)


class MessageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializers

    def create(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(owner_id=request.user.id)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializers

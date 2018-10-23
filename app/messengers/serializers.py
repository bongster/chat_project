from django.db.models import Q
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Room, Message, Room2User

# AttributeError: Manager isn't available; 'auth.User' has been swapped for 'users.user'
from django.contrib.auth import get_user_model


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email')


class RoomSerializers(serializers.ModelSerializer):
    participated_user = UserSerializers(required=False, many=True)
    latest_msg = serializers.CharField(read_only=True)

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

        participated_user = validated_data.get('participated_user')
        if participated_user:
            for user in participated_user:
                Room2User.objects.create(
                    room_id=instance.id,
                    user_id=user.id,
                )

        return instance

    def to_representation(self, instance):
        users = UserSerializers(
            get_user_model().objects.filter(
                pk__in=Room2User.objects.filter(
                    room_id=instance.id
                ).values_list('user_id', flat=True)
            ),
            many=True,
        )

        instance.participated_user = users.data
        latest_msg = Message.objects.filter(
            room_id=instance.id
        ).order_by('id').last()

        if latest_msg:
            instance.latest_msg = latest_msg.msg

        return super().to_representation(instance)


class MessageSerializers(serializers.ModelSerializer):
    user_name = serializers.CharField(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'

    def create(self, validated_data):
        # TODO: create message for paticiated_users
        validated_data['owner_id'] = validated_data.get('owner_id') or self.context['request'].user.id
        instance = super().create(validated_data)
        # Update room update_at field when create message row
        Room.objects.get(
            pk=instance.room_id,
        ).save(update_fields=['updated_at'])
        return instance

    def to_representation(self, instance):
        instance.user_name = get_user_model().objects.get(pk=instance.owner_id)
        return super().to_representation(instance)


class Room2UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = Room2User
        fields = '__all__'


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializers

    @action(methods=['POST'], detail=True, url_path='users')
    def add_user_2_room(self, request, pk=None):
        # TODO make
        serializer = Room2UserSerializers(data=request.data, context= {'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(methods=['DELETE'], detail=True, url_path='users')
    def delete_user_2_room(self, request, pk=None):
        serializer = Room2UserSerializers(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.update(
                is_active=False
            )
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response()

    def create(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.owner_id = request.user.id

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

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializers


class Room2UserViewSet(viewsets.ModelViewSet):
    queryset = Room2User.objects.all()
    serializer_class = Room2UserSerializers

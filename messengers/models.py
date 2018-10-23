from django.db import models

# Create your models here.


class Room(models.Model):
    class Meta:
        db_table = 'rooms'
        index_together = (
            ('owner_id', 'is_active'),
        )
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    owner_id = models.PositiveIntegerField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class Room2User(models.Model):
    class Meta:
        db_table = 'rooms_to_users'
        unique_together = (
            ('room_id', 'user_id'),
        )

    room_id = models.IntegerField()
    user_id = models.IntegerField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class Message(models.Model):
    class Meta:
        db_table = 'messages'

    owner_id = models.PositiveIntegerField(db_index=True, blank=True)
    room_id = models.PositiveIntegerField(db_index=True)

    msg = models.TextField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

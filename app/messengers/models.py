from django.db import models

# Create your models here.

class Romm(models.Model):
    class Meta:
        db_table = 'rooms'
        index_together = (
            ('owner_id', 'is_active'),
        )
    name=models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    owner_id = models.PositiveIntegerField(null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=False)

class Message(models.Model):
    class Meta:
        db_table = 'messages'

    form_user = models.PositiveIntegerField(db_index=True)
    to_user = models.PositiveIntegerField(db_index=True)

    created_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=False)

    is_active = models.BooleanField(default=True)

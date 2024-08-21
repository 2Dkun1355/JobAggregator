from django.db import models
from django.contrib.auth.models import User


class AdditionalUserFields(models.Model):
    user = models.OneToOneField(
        to=User,
        related_name='additional',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    telegram_id = models.CharField(
        max_length=64,
        null=True,
        blank=True,
    )
    telegram_chat_id = models.CharField(
        max_length=64,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.user.username if self.user else self.id



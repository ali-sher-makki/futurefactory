from django.db import models


class PushSubscription(models.Model):
    endpoint = models.URLField(unique=True, max_length=500)
    p256dh = models.CharField(max_length=255)
    auth = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.endpoint[:50]
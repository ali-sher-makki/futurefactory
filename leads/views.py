import json
import logging
import os
import time
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.conf import settings
from pywebpush import webpush, WebPushException

from .models import Lead
from .serializers import LeadSerializer
from core.models import PushSubscription

logger = logging.getLogger(__name__)


class LeadCreateView(generics.CreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lead = serializer.save()
        self.notify_admin_email(lead)
        self.notify_admin_push(lead)
        return Response(
            {'success': True, 'message': "Thanks! We'll be in touch within 24 hours."},
            status=status.HTTP_201_CREATED,
        )

    def notify_admin_email(self, lead):
        if not getattr(settings, 'ADMIN_EMAIL', ''):
            return
        subject = f"New lead: {lead.name}"
        message = (
            f"Name: {lead.name}\n"
            f"Email: {lead.email}\n"
            f"Phone: {lead.phone or '-'}\n"
            f"Company: {lead.company or '-'}\n"
            f"Interested in: {lead.service_interested or '-'}\n\n"
            f"Message:\n{lead.message}"
        )
        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL], fail_silently=True)
        except Exception:
            logger.exception("Failed to send lead notification email")

    def notify_admin_push(self, lead):
        if not settings.VAPID_PUBLIC_KEY:
            logger.warning("VAPID_PUBLIC_KEY not set — skipping push notification")
            return

        subscriptions = PushSubscription.objects.all()
        if not subscriptions.exists():
            logger.warning("No push subscriptions found — no one is subscribed to receive alerts")
            return

        # Read the private key file content rather than passing a file path.
        # Passing a path can fail with pywebpush on Windows when the path
        # contains spaces (e.g. "future factory").
        private_key_path = str(settings.BASE_DIR / settings.VAPID_PRIVATE_KEY_PATH)
        if not os.path.isfile(private_key_path):
            logger.error(f"VAPID private key file not found at {private_key_path}")
            return
        logger.info(f"Using VAPID private key at {private_key_path}")

        payload = json.dumps({
            'title': f'New lead: {lead.name}',
            'body': lead.message[:100],
            'url': '/admin/leads/lead/',
        })

        logger.info(f"Sending push notifications to {subscriptions.count()} subscription(s)")

        for sub in subscriptions:
            subscription_info = {
                'endpoint': sub.endpoint,
                'keys': {'p256dh': sub.p256dh, 'auth': sub.auth},
            }
            try:
                webpush(
                    subscription_info=subscription_info,
                    data=payload,
                    vapid_private_key=private_key_path,
                    vapid_claims={
                        'sub': settings.VAPID_CLAIM_EMAIL,
                        'exp': int(time.time()) + 86400,
                    },
                )
                logger.info(f"Push sent successfully to subscription {sub.id}")
            except WebPushException as e:
                status_code = e.response.status_code if e.response is not None else 'unknown'
                logger.warning(f"Push failed for subscription {sub.id}: status={status_code}, error={e}")
                if e.response is not None and e.response.status_code == 410:
                    sub.delete()
                    logger.info(f"Deleted expired subscription {sub.id}")
            except Exception as e:
                logger.exception(f"Unexpected error sending push to subscription {sub.id}: {e}")
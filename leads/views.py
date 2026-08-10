from rest_framework import generics, status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .models import Lead
from .serializers import LeadSerializer


class LeadCreateView(generics.CreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lead = serializer.save()
        self.notify_admin(lead)
        return Response(
            {'success': True, 'message': "Thanks! We'll be in touch within 24 hours."},
            status=status.HTTP_201_CREATED,
        )

    def notify_admin(self, lead):
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
            pass
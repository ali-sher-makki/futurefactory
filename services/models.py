from django.db import models
from django.urls import reverse


class Service(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=110, unique=True)
    icon = models.CharField(max_length=10, blank=True, help_text="Single emoji shown on the card, e.g. 🎯")
    short_description = models.CharField(max_length=160)
    detail_description = models.TextField()
    features = models.TextField(blank=True, help_text="One feature per line")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('services:detail', kwargs={'slug': self.slug})

    def feature_list(self):
        return [f.strip() for f in self.features.splitlines() if f.strip()]
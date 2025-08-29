from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings


class Source(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Quote(models.Model):
    text = models.TextField(unique=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='quotes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    weight = models.PositiveSmallIntegerField(default=1)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'"{self.text}" - {self.author}'

    def presave(self):
        max_count = settings.SOURCE_QUOTE_LIMIT
        if Quote.objects.filter(source=self.source).exclude(pk=self.pk).count() >= max_count:
            raise ValidationError(f"Максимум {max_count} записей для категории {self.source}")

    def save(self, *args, **kwargs):
        self.presave()
        super().save(*args, **kwargs)

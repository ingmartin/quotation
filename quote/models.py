from django.db import models
from django.core.exceptions import ValidationError


class Source(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Quote(models.Model):
    text = models.TextField(unique=True)
    author = models.CharField(max_length=255)
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='quotes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    weight = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'"{self.text}" - {self.author}'

    def clean(self):
        max_count = 3
        if Quote.objects.filter(source=self.source).exclude(pk=self.pk).count() >= max_count:
            raise ValidationError(f"Максимум {max_count} записей для категории {self.source}")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

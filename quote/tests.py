from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Quote, Source


class QuoteModelTests(TestCase):

    def setUp(self):
        # создаём источние "fun"
        src = Source.objects.create(name="fun")
        # создаём 3 записи с указанием источника "fun"
        for i in range(3):
            Quote.objects.create(text=f"Quote {i}", author="Paulo", source=src)

    def test_can_create_up_to_limit(self):
        """Можно создать ровно 3 записи с указанием одного источника"""
        src = Source.objects.get_or_create(name="fun")[0]
        self.assertEqual(Quote.objects.filter(source=src).count(), 3)

    def test_cannot_create_more_than_limit(self):
        """Попытка создать 4-ю запись вызывает ValidationError"""
        src = Source.objects.get_or_create(name="fun")[0]
        q = Quote(text="extra", author="Paulo", source=src)
        with self.assertRaises(ValidationError):
            q.save()

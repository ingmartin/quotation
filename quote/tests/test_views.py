import pytest
from django.urls import reverse
from django.test import Client
from quote.models import Source, Quote


@pytest.mark.django_db
class TestQuoteViews:

    def setup_method(self):
        self.client = Client()
        self.source = Source.objects.create(name="Test Source")
        self.quote = Quote.objects.create(text="Test Quote", source=self.source, weight=5)

    def test_quote_list(self):
        url = reverse("quote_list")
        resp = self.client.get(url)
        assert resp.status_code == 200
        assert "Test Quote" in resp.content.decode()

    def test_quote_create(self):
        url = reverse("quote_create")
        resp = self.client.post(url, {
            "text": "Another Quote",
            "source_name": "Test Source",
            "weight": 3,
        })
        assert resp.status_code == 302
        assert Quote.objects.filter(text="Another Quote").exists()

    def test_quote_update(self):
        url = reverse("quote_update", args=[self.quote.id])
        resp = self.client.post(url, {
            "text": "Updated Quote",
            "source_name": "Test Source",
            "weight": 7,
        })
        assert resp.status_code == 302
        self.quote.refresh_from_db()
        assert self.quote.text == "Updated Quote"

    def test_quote_delete(self):
        url = reverse("quote_delete", args=[self.quote.id])
        resp = self.client.post(url)
        assert resp.status_code == 302
        assert not Quote.objects.filter(id=self.quote.id).exists()

    def test_quote_like(self):
        url = reverse("quote_like", args=[self.quote.id])
        resp = self.client.post(url)
        assert resp.status_code == 302
        self.quote.refresh_from_db()
        assert self.quote.likes == 1

    def test_quote_dislike(self):
        url = reverse("quote_dislike", args=[self.quote.id])
        resp = self.client.post(url)
        assert resp.status_code == 302
        self.quote.refresh_from_db()
        assert self.quote.dislikes == 1

    def test_quote_dashboard(self):
        url = reverse("quote_hits")
        resp = self.client.get(url)
        assert resp.status_code == 200
        assert "Test Quote" in resp.content.decode()

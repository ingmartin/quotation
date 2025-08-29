from django.urls import path
from .views import (
    RandomQuoteView, QuoteListView, QuoteCreateView, QuoteUpdateView, QuoteDeleteView,
    quote_like, quote_dislike, quote_dashboard
)

urlpatterns = [
    path('', RandomQuoteView.as_view(), name="random_quote"),
    path('list/', QuoteListView.as_view(), name="quote_list"),
    path('add/', QuoteCreateView.as_view(), name="quote_create"),
    path('dashboard/', quote_dashboard, name="quote_hits"),
    path('update/<int:pk>/', QuoteUpdateView.as_view(), name="quote_update"),
    path("delete/<int:pk>/", QuoteDeleteView.as_view(), name="quote_delete"),
    path("like/<int:pk>/", quote_like, name="quote_like"),
    path("dislike/<int:pk>/", quote_dislike, name="quote_dislike"),
]

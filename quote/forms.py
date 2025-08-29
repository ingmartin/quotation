from django import forms
from .models import Quote


class QuoteForm(forms.ModelForm):
    source_name = forms.CharField(max_length=255, required=False, label="Источник")

    class Meta:
        model = Quote
        fields = ["text", "weight"]

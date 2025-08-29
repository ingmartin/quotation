import random
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views.generic import ListView, View, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Quote, Source
from .forms import QuoteForm


class QuoteListView(ListView):
    model = Quote
    template_name = 'quote/quote_list.html'
    context_object_name = 'quotes'
    paginate_by = 10

    def get_queryset(self):
        return Quote.objects.all().order_by('-created_at')


class SourceListView(ListView):
    model = Source
    template_name = 'quote/source_list.html'
    context_object_name = 'sources'
    paginate_by = 10

    def get_queryset(self):
        return Quote.objects.all().order_by('-id')


class RandomQuoteView(View):
    model = Quote
    template_name = 'quote/random_quote.html'
    context_object_name = 'quote'

    def get(self, request, *args, **kwargs):
        quotes = list(Quote.objects.all())
        if not quotes:
            quote = Quote.objects.none()
        else:
            weights = [q.weight for q in quotes]
            quote = random.choices(quotes, weights=weights, k=1)[0]
            quote.views += 1
            quote.save()
        return render(
            request,
            self.template_name,
            {
                self.context_object_name: quote,
            }
        )


class QuoteCreateView(CreateView):
    model = Quote
    template_name = "quote/quote_form.html"
    form_class = QuoteForm
    success_url = reverse_lazy("random_quote")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["sources"] = Source.objects.all()
        ctx["source_name"] = self.request.GET.get("source_name", "")
        return ctx

    def form_valid(self, form):
        self.object = form.save(commit=False)
        source_name = form.cleaned_data.get("source_name").strip()
        if source_name:
            source, _ = Source.objects.get_or_create(name=source_name)
            self.object.source = source
        else:
            form.add_error("source_name", "Укажите источник.")
            return self.form_invalid(form)
        self.object.clean()
        try:
            self.object.presave()
        except ValidationError as e:
            form.add_error('source_name', e.message)
            return self.form_invalid(form)
        self.object.save()
        return super().form_valid(form)


class QuoteUpdateView(UpdateView):
    model = Quote
    template_name = "quote/quote_form.html"
    form_class = QuoteForm
    success_url = reverse_lazy("quote_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["sources"] = Source.objects.all()
        ctx["source_name"] = self.object.source.name if self.object.source else ""
        return ctx

    def form_valid(self, form):
        self.object = form.save(commit=False)
        source_name = form.cleaned_data.get("source_name").strip()
        if source_name:
            source, _ = Source.objects.get_or_create(name=source_name)
            self.object.source = source
        else:
            raise ValidationError("Source name cannot be empty.")
        self.object.clean()
        self.object.presave()
        self.object.save()
        return super().form_valid(form)


class QuoteDeleteView(DeleteView):
    model = Quote
    template_name = "quote/quote_confirm_delete.html"
    success_url = reverse_lazy("quote_list")


def quote_like(request, pk):
    quote = Quote.objects.get(pk=pk)
    quote.likes += 1
    quote.save()
    return redirect('random_quote')


def quote_dislike(request, pk):
    quote = Quote.objects.get(pk=pk)
    quote.dislikes += 1
    quote.save()
    return redirect('random_quote')


def quote_dashboard(request):
    all_quotes = Quote.objects.all()
    quotes = dict()
    quotes["hits"] = all_quotes.order_by('-views')[:10]
    quotes["rare"] = all_quotes.order_by('views')[:10]
    quotes["liked"] = all_quotes.order_by('-likes')[:10]
    quotes["disliked"] = all_quotes.order_by('-dislikes')[:10]
    return render(request, 'quote/quote_dashboard.html', {'quotes': quotes})

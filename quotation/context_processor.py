from django.conf import settings


def global_settings(request):
    return {
        "SOURCE_QUOTE_LIMIT": settings.SOURCE_QUOTE_LIMIT,
        "APP_NAME": "Quotation Book",
    }

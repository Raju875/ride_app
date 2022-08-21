from django.apps import AppConfig


class StripeAppConfig(AppConfig):
    name = 'stripe_app'

    def ready(self):
        try:
            import stripe_app.signals
        except ImportError:
            pass

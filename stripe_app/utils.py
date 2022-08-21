from django.conf import settings
import stripe
from stripe.error import StripeError

from .models import *

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_customer(user):
    try:
        stripe_customer = stripe.Customer.create(
            name=user.username,
            email=user.email,
            metadata={
                'user_id': user.id
            }
        )
    except Exception as e:
        print(e)
        stripe_customer = None

    return stripe_customer


def app_create_stripe_customer(user):
    try:
        stripe_customer = create_stripe_customer(user)
    except StripeError as e:
        print(e)
        return None
    if stripe_customer:
        from .models import StripeCustomer
        customer = StripeCustomer.objects.create(
            user_id=user.id,
            customer_id=stripe_customer.id,
            name=stripe_customer.name,
            email=stripe_customer.email,
            phone=user.customer_profile.phone if user.user_type == 2 else user.driver_profile.phone,
            user_type=user.user_type,
            currency='usd',
        )
        return customer
    return None


def stripe_customer_details(customer_id):
    try:
        customer = stripe.Customer.retrieve(customer_id)
    except Exception as e:
        print(e)
        customer = None
    return customer


def stripe_customer_delete(customer_id, user_id=None):
    return stripe.Customer.delete(customer_id)


def create_card_token(data, customer=None):
    return stripe.Token.create(
        card={
            "number": data['number'],
            "name": data['name'],
            "exp_month": data['exp_month'],
            "exp_year": data['exp_year'],
            "cvc": data['cvc'],
        },
        customer=customer
    )


def retrieve_card_token(token):
    return stripe.Token.retrieve(token)


def create_customer_source(customer_id, source_id, user=None):
    metadata = {}
    if user:
        metadata['user_id'] = user.id
    return stripe.Customer.create_source(customer_id, source=source_id, metadata=metadata)


def delete_customer_source(customer_id, source_id):
    return stripe.Customer.delete_source(customer_id, source_id)

def create_payment_method(payment_method, method_type):
    try:
        stripe_method = stripe.PaymentMethod.create(
            type=method_type,
            card=payment_method
        )
    except Exception as e:
        print(e)
        stripe_method = None

    return stripe_method


def attach_payment_method(payment_method, customer):
    return stripe.PaymentMethod.attach(payment_method, customer=customer)


def create_stripe_charge(source, amount, currency='usd', capture=False, receipt_email=None, customer=None,
                         metadata=None or dict):
    print(metadata)
    stripe_metadata = {}
    if metadata is not None:
        stripe_metadata = metadata
    return stripe.Charge.create(
        amount=amount, source=source, currency=currency, capture=capture, receipt_email=receipt_email,
        customer=customer, metadata=stripe_metadata
    )


def create_payment_intent(amount, payment_method, confirm=False, capture_method='automatic',
                          customer=None, metadata={}, receipt_email=''):
    return stripe.PaymentIntent.create(
        amount=amount,
        currency="usd",
        payment_method_types=["card"],
        confirm=confirm,
        payment_method=payment_method,
        customer=customer,
        metadata=metadata,
        receipt_email=receipt_email,
        capture_method=capture_method,
    )


def retrieve_payment_intent(payment_intent):
    return stripe.PaymentIntent.retrieve(payment_intent)


def capture_payment_intent(payment_intent, amount=0):
    return stripe.PaymentIntent.capture(payment_intent)

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from stripe.error import StripeError, CardError

from stripe_app.models import *
from stripe_app.utils import create_card_token, retrieve_card_token,  app_create_stripe_customer, create_customer_source


class StripeCustomerSerializer(serializers.ModelSerializer):
    api_details = serializers.JSONField(read_only=True)

    class Meta:
        model = StripeCustomer
        fields = '__all__'


class CardTokenCreateSerializer(serializers.Serializer):
    number = serializers.CharField(max_length=16, required=True, write_only=True)
    name = serializers.CharField(max_length=100, required=True, write_only=True)
    exp_month = serializers.IntegerField(required=True, write_only=True)
    exp_year = serializers.IntegerField(required=True, write_only=True)
    cvc = serializers.CharField(max_length=3, required=True, write_only=True)

    def create(self, validated_data):
        try:
            token = create_card_token(data=validated_data)
        except CardError as e:
            print(e.user_message)
            raise serializers.ValidationError({'error': _(e.user_message)})

        return token


class CustomerPaymentSourceSerializer(serializers.ModelSerializer):
    source = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomerPaymentSource
        fields = '__all__'

        extra_kwargs = {
            'source_id': {
                'read_only': True
            },
            'details': {
                'read_only': True
            },
            'customer': {
                'read_only': True
            },
            'fingerprint': {
                'read_only': True
            }
        }


    def create(self, validated_data):
        request_user = self.context['request'].user
        source = validated_data.pop('source')
        is_default = validated_data.pop('is_default')
        customer_id = None
        try:
            customer = request_user.stripe_customer
            customer_id = customer.customer_id
        except StripeCustomer.DoesNotExist:
            customer = app_create_stripe_customer(request_user)
            customer_id = customer.customer_id
        except Exception as e:
            print(e)

        if not customer_id:
            raise serializers.ValidationError( _('Payment source create failed for this customer'))
        try:
            token_details = retrieve_card_token(source)
        except StripeError as e:
            print(e)
            raise serializers.ValidationError({'source': _('Invalid token.')})
        if token_details:
            check_exists = CustomerPaymentSource.objects.filter(customer=customer,
                                                                fingerprint=token_details.card.fingerprint).exists()
            if check_exists:
                raise serializers.ValidationError(_('You already have this card saved.'))
        try:
            source_content = create_customer_source(customer_id, source, user=request_user)
        except StripeError as e:
            print(e)
            raise serializers.ValidationError({'error': _(e.user_message)})
        except Exception as e:
            raise serializers.ValidationError({'error': _('Source token error')})

        if is_default:
            CustomerPaymentSource.objects.filter(customer=customer).update(is_default=False)
        customer_source = CustomerPaymentSource.objects.create(source_id=source_content.id,
                                                                customer=customer,
                                                                details=source_content,
                                                                is_default=is_default,
                                                                fingerprint=source_content.fingerprint)
                                                                
        return customer_source
        

class CustomerPaymentSourceUpdateSerializer(serializers.ModelSerializer):
    is_default = serializers.BooleanField(required=True)

    class Meta:
        model = CustomerPaymentSource
        fields = '__all__'

        extra_kwargs = {
            'source_id': {
                'read_only': True
            },
            'details': {
                'read_only': True
            },
            'customer': {
                'read_only': True
            },
            'fingerprint': {
                'read_only': True
            }
        }

    def update(self, instance, validated_data):
        print(12121)
        request_user = self.context['request'].user
        customer = request_user.stripe_customer
        is_default = validated_data.get('is_default')
        if is_default:
            CustomerPaymentSource.objects.filter(customer=customer).update(is_default=False)
        return super().update(instance, validated_data)
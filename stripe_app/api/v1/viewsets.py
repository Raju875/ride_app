from django.utils.translation import ugettext_lazy as _
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import views, viewsets, permissions, status
from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404
    
from .serializers import *
from stripe_app.utils import delete_customer_source


class StripeConfiguration(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, ]

    def get(request, *args, **kwargs):
        from django.conf import settings
        try:
            publishable_key = settings.STRIPE_PUBLISHABLE_KEY
        except Exception as e:
            return Response({'error': _(str(e))}, status=status.HTTP_404_NOT_FOUND)
            
        return Response({'publishable_key': publishable_key})


class MyCystomerAccount(RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = StripeCustomerSerializer
    queryset = StripeCustomer.objects.all()

    def get_object(self):
        return get_object_or_404(self.get_queryset(), user=self.request.user)


class CustomerPaymentSourceAPIView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = CustomerPaymentSourceSerializer
    queryset = CustomerPaymentSource.objects.none()

    def get_serializer_class(self):
        if self.action == 'update':
            return CustomerPaymentSourceUpdateSerializer
        return CustomerPaymentSourceSerializer

    def get_queryset(self):
        return CustomerPaymentSource.objects.filter(customer__user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj:
            raise serializers.ValidationError({'error': _('Payment source not found!')})
        # if obj.is_default:
        #     raise serializers.ValidationError({'error': _('Default card cannot be removed. Change default card & try again.')})
        try:
            delete_customer_source(obj.customer.customer_id, obj.source_id)
            obj.delete()
            return Response({'success': _('Card remvove successfully')}, status=status.HTTP_204_NO_CONTENT)
        except StripeError as e:
            raise serializers.ValidationError({'error': _(e.user_message + '[SA-101]')})
        except Exception as e:
            raise serializers.ValidationError({'error': _(str(e) + '[SA-102]')})

    
    @action(detail=False, methods=['post'])
    def create_token(self, request):
        request_data = request.data
        try:
            request.user.stripe_customer
        except StripeCustomer.DoesNotExist as err:
            raise serializers.ValidationError({'error': _(str(err) + '[SA-103]')})
            app_create_stripe_customer(request.user)
        serializer = CardTokenCreateSerializer(data=request_data, context={'request': request})
        if serializer.is_valid():
            data = serializer.save()
            return Response(data)
        return Response(serializer.errors)

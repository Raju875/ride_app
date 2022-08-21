from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField

from stripe_app.utils import stripe_customer_details


class StripeCustomer(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='stripe_customer')
    customer_id = models.CharField(max_length=256)
    name = models.EmailField(max_length=256)
    email = models.EmailField(max_length=256)
    phone = models.CharField(max_length=20, default=None, null=True, blank=True)
    user_type = models.IntegerField()
    currency = models.CharField(default="", max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.customer_id

    class Meta:
        ordering = ('user__username', '-created_at',)
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')

    def api_details(self):
        return stripe_customer_details(self.customer_id)


class CustomerPaymentSource(models.Model):
    source_id = models.CharField(_('Source ID'), max_length=255, unique=True)
    customer = models.ForeignKey('StripeCustomer', on_delete=models.SET_NULL, null=True, blank=True, related_name='payment_source')
    is_default = models.BooleanField(_('Default'), default=False)
    details = JSONField(blank=True, null=True, default=dict)
    fingerprint = models.CharField(_('Fingerprint'), max_length=120, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.source_id

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Customer Payment Source')
        verbose_name_plural = _('Customer Payment Sources')
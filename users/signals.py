from stripe_app.utils import app_create_stripe_customer
from stripe_app.models import StripeCustomer
from users.models import CustomerDocuments, CustomerProfile, DriverProfile, VehicleInfo
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.conf import settings
from django.template.loader import render_to_string

from django.contrib.auth import get_user_model
User = get_user_model()


@receiver(post_save, sender=CustomerProfile)
@receiver(post_save, sender=DriverProfile)
def post_save_profile(sender, instance, *args, **kwargs):
    """ Update user info  and send verify mail"""
    try:
        User.objects.filter(id=instance.user_id).update(
            email=instance.email,
            name=instance.full_name
        )

        if instance.__class__.__name__ == 'CustomerProfile':
            CustomerDocuments.objects.filter(
                user=instance.user).update(customer=instance)

        # verify mail send to user
        if instance.is_approved and not instance.is_verify_mail_sent:
            email_context = {
                "email": instance.email
            }
            html_content = render_to_string(
                'profile_verify.html', email_context)
            message = Mail(
                from_email=settings.DEFAULT_FROM_EMAIL,
                to_emails=instance.email,
                subject='Profile Verify',
                html_content=html_content)
            sg = SendGridAPIClient(settings.EMAIL_HOST_PASSWORD)
            sg.send(message)

            instance.is_verify_mail_sent = True
            instance.save()

            # create stripe customer if not exists
            try:
                instance.user.stripe_customer
            except StripeCustomer.DoesNotExist:
                app_create_stripe_customer(user=instance.user)

    except Exception as e:
        print(e)


# def get_file(file):
#     file_path = os.path.join(settings.MEDIA_ROOT, file)
#     if os.path.exists(file_path):
#         return file_path
#     else:
#         return None


# def os_remove_file(new_file, old_file):
#     if not old_file:
#         return False
#     old_file_path = get_file(old_file)
#     if old_file_path:
#         if not new_file or (new_file.name.split('/')[-1] != old_file_path.split('/')[-1]):
#             os.remove(old_file_path)


# def get_file_and_remove(file):
#     if not file:
#         return False
#     file_path = os.path.join(settings.MEDIA_ROOT, file)
#     if os.path.exists(file_path):
#         os.remove(file_path)


# @receiver(pre_save, sender=CustomerProfile)
# @receiver(pre_save, sender=DriverProfile)
# @receiver(pre_save, sender=VehicleInfo)
# def pre_save_profile(sender, instance, *args, **kwargs):
#     """
#     Clean old document's file
#     instance have id only during the update/delete
#     """
#     try:
#         if instance.user.user_type == 2:  # Customer
#             data = CustomerProfile.objects.get(id=instance.id)
#             os_remove_file(instance.document_front_photo,
#                            data.document_front_photo.name)
#             os_remove_file(instance.document_back_photo,
#                            data.document_back_photo.name)
#             os_remove_file(instance.face_photo, data.face_photo.name)
#             os_remove_file(instance.profile_image, data.profile_image.name)

#         elif instance.user.user_type == 3:  # Driver

#             if instance.__class__.__name__ == 'DriverProfile':
#                 data = DriverProfile.objects.get(id=instance.id)
#                 os_remove_file(instance.profile_image, data.profile_image.name)
#                 os_remove_file(instance.address_photo, data.address_photo.name)
#                 os_remove_file(instance.license_front_photo,
#                                data.license_front_photo.name)
#                 os_remove_file(instance.license_back_photo,
#                                data.license_back_photo.name)
#                 os_remove_file(instance.identity_document_front_photo,
#                                data.identity_document_front_photo.name)
#                 os_remove_file(instance.identity_document_back_photo,
#                                data.identity_document_back_photo.name)

#             if instance.__class__.__name__ == 'VehicleInfo':
#                 data = VehicleInfo.objects.get(id=instance.id)
#                 os_remove_file(instance.mvr_document, data.mvr_document.name)
#                 os_remove_file(instance.insurance_document,
#                                data.insurance_document.name)
#                 os_remove_file(instance.operating_card_document,
#                                data.operating_card_document.name)
#                 os_remove_file(instance.inspection_document,
#                                data.inspection_document.name)
#                 os_remove_file(instance.image, data.image.name)

#     except Exception as e:
#         import sys
#         _type, _object, _traceback = sys.exc_info()
#         filename = _traceback.tb_frame.f_code.co_filename
#         line_number = _traceback.tb_lineno

#         print("Exception type: ", _type)
#         print("File name: ", filename)
#         print("Line number: ", line_number)
#         print("Exception: ", e)


# @receiver(pre_delete, sender=CustomerProfile)
# @receiver(pre_delete, sender=DriverProfile)
# @receiver(pre_delete, sender=VehicleInfo)
# def pre_delete_profile(sender, instance, *args, **kwargs):
#     """ Clean document's file """
#     try:
#         if instance.user.user_type == 2:  # Customer
#             data = CustomerProfile.objects.get(id=instance.id)

#             get_file_and_remove(data.document_front_photo.name)
#             get_file_and_remove(data.document_back_photo.name)
#             get_file_and_remove(data.face_photo.name)
#             get_file_and_remove(data.profile_image.name)

#         elif instance.user.user_type == 3:  # Driver=

#             if instance.__class__.__name__ == 'DriverProfile':
#                 get_file_and_remove(instance.profile_image)
#                 get_file_and_remove(instance.address_photo)
#                 get_file_and_remove(instance.license_front_photo)
#                 get_file_and_remove(instance.license_back_photo)
#                 get_file_and_remove(instance.identity_document_front_photo)
#                 get_file_and_remove(instance.identity_document_back_photo)

#             if instance.__class__.__name__ == 'VehicleInfo':
#                 get_file_and_remove(instance.mvr_document.name)
#                 get_file_and_remove(instance.insurance_document.name)
#                 get_file_and_remove(instance.operating_card_document.name)
#                 get_file_and_remove(instance.inspection_document.name)
#                 get_file_and_remove(instance.image.name)

#     except Exception as e:
#         import sys
#         _type, _object, _traceback = sys.exc_info()
#         filename = _traceback.tb_frame.f_code.co_filename
#         line_number = _traceback.tb_lineno

#         print("Exception type: ", _type)
#         print("File name: ", filename)
#         print("Line number: ", line_number)
#         print("Exception: ", e)

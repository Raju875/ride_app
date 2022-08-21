import os.path
from django.utils import timezone
from rest_framework import serializers
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.files.uploadedfile import UploadedFile
from datetime import datetime


import base64
import uuid
from django.core.files.base import ContentFile
from rest_framework import serializers

# Custom image field - handles base 64 encoded images
class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if not data:
           return False
        if isinstance(data, str) and data.startswith('data:image'):
            # base64 encoded image - decode
            format, imgstr = data.split(';base64,')  # format ~= data:image/X,
            ext = format.split('/')[-1]  # guess file extension
            id = uuid.uuid4()
            data = ContentFile(base64.b64decode(imgstr),
                               name=id.urn[9:] + '.' + ext)
        return super(Base64ImageField, self).to_internal_value(data)



def file_validation(value):
    """
    Common image/attachment validation check
    """
    if value and isinstance(value, UploadedFile):
        # MIME_TYPE = ['jpg', 'jpeg', 'png', 'pdf', 'doc']
        # file_type = value.content_type.split('/')[-1]
        # if file_type not in MIME_TYPE:
        #     raise serializers.ValidationError(
        #         _('{file_type} file not supported. Please upload image, pdf or doc file'.format(
        #             file_type=file_type.upper())))

        MAX_UPLOAD_SIZE = 2
        file_size = value.size/(1024*1024)
        if file_size > MAX_UPLOAD_SIZE:
            raise serializers.ValidationError(
                _('Please keep filesize under {MAX_UPLOAD_SIZE}MB. Current filesize {file_size}MB').format(
                    MAX_UPLOAD_SIZE=MAX_UPLOAD_SIZE, file_size=round(file_size, 3)))
    else:
        pass


def file_upload(instance, filename, *args, **kwargs):
    """
    Common image/attachment upload
    """
    from django.utils import timezone
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    new_filename = f"{now:%d%H%M%S}-{now.microsecond}{extension}"
    dir_name = instance.__class__.__name__.lower()
    file_path = f"uploads/user_{instance.user_id}/{dir_name}"
    return os.path.join(file_path, new_filename)


from pytz import timezone
class TimeZoneUtil():
    @staticmethod
    def utc_to_timezone(datetime=None):
        settings_time_zone = timezone(settings.TIME_ZONE)
        return datetime.astimezone(settings_time_zone)

    @staticmethod
    def get_datetime():
        now = datetime.now()
        settings_time_zone = timezone(settings.TIME_ZONE)

        return now.astimezone(settings_time_zone)

    @staticmethod
    def seconds_to_hours(seconds=None):
        hours = seconds // 3600
        minutes = seconds // 60 - hours * 60
        
        result = "%d:%02d" % (hours, minutes)

        return result
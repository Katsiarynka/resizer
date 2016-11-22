from rest_framework import serializers

from images.utils import validate_img
from .models import Image
from .tasks import resize
from resizer.utils import publish_in_ws

IMAGE_MIME_TYPES = ("image/jpeg", "image/png", "image/tiff")


class UnsupportedImageFormat(serializers.ValidationError):
    pass


class ImageSerializer(serializers.ModelSerializer):
    original_image = serializers.FileField(required=True, use_url=False)
    original_url = serializers.SerializerMethodField()
    converted_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ('id', 'original_url', 'converted_url', 'created', 'converted_datetime', 'original_image')
        read_only_fields = 'created', 'converted_datetime'

    def get_original_url(self, obj):
        return obj.original_image.url if obj.original_image.name else ''

    def get_converted_url(self, obj):
        return obj.converted_image.url if obj.converted_image.name else ''

    def validate_original_image(self, file):
        validate_img(file, 'original_image')
        return file

    def create(self, validated_data):
        original_image = validated_data.get('original_image')
        image = Image.objects.create(original_image=original_image)
        publish_in_ws(image)
        job = resize.delay(image.id)
        image.job_id = job.id
        image.save()
        return image

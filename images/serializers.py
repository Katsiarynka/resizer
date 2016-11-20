
from rest_framework import serializers

from .models import Image
from .tasks import resize


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'original', 'created', 'converted_datetime')
        read_only_fields = ['created', 'converted_datetime', ]

    def create(self, validated_data):
        original = validated_data.get('original')
        image = Image.objects.create(original=original)
        job = resize.delay(image.id)
        image.job_id = job.id
        image.save()
        return image


from rest_framework import serializers

from images.models import Image


class ViewImage(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['id', 'created', 'converted_datetime', ]

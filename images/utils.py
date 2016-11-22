import os

import magic
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import serializers

from resizer.settings import MEDIA_ROOT

IMAGE_MIME_TYPES = ("image/jpeg", "image/png")


class UnsupportedImageFormat(serializers.ValidationError):
    pass


def validate_img(file, key):
    path = default_storage.save('tmp/'+file.name, ContentFile(file.read()))
    tmp_file = os.path.join(MEDIA_ROOT, path)
    try:
        mimetype = magic.from_file(tmp_file, mime=True)
        if not mimetype in IMAGE_MIME_TYPES:
            raise UnsupportedImageFormat({key: "Unsupported image format {}".format(mimetype)})
    finally:
        os.remove(tmp_file)

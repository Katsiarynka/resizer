import os

from django.db import models

from resizer.settings import MEDIA_ROOT, MEDIA_URL

LOADED = 'loaded'
FAILED = 'failed'
CONVERTED = 'converted'
DIR_ORIGINAL = 'images/original'
DIR_CONVERTED = 'images/converted'


class Image(models.Model):
    original_image = models.ImageField(upload_to=MEDIA_ROOT + DIR_ORIGINAL)
    converted_image = models.ImageField(upload_to=MEDIA_ROOT + DIR_CONVERTED)
    converted_datetime = models.DateTimeField(null=True)
    status = models.CharField(max_length=25)
    job_id = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    issues = models.TextField(null=True)

    def save(self, *args, **kwargs):
        return super(Image, self).save(*args, **kwargs)

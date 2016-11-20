from __future__ import unicode_literals

from django.db import models

LOADED = 'loaded'
CONVERTED = 'converted'
DIR_ORIGINAL = 'original'
DIR_CONVERTED = 'converted'


class Image(models.Model):
    original = models.CharField(max_length=100)
    status = models.CharField(max_length=25)
    converted_image = models.CharField(max_length=100)
    converted_datetime = models.DateTimeField(null=True)
    job_id = models.CharField(max_length=16)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.converted_image:
            self.status = CONVERTED
        elif self.original:
            self.status = LOADED
        return super(Image, self).save(*args, **kwargs)
from django.utils.timezone import now

from resizer.celery import app
from PIL import Image as PilImage

from images.models import Image, FAILED, CONVERTED, DIR_CONVERTED
from resizer.settings import MEDIA_ROOT

WEIGHT = 2


@app.task
def resize(image_id):
    image = Image.objects.get(id=image_id)
    try:
        original = PilImage.open(image.original)
        converted = original.resize([original.width/WEIGHT, original.height/WEIGHT])
        path = MEDIA_ROOT + DIR_CONVERTED + '/' + image.original.name.split('/')[-1]
        converted.save(path)
        image.converted_image = path
        image.converted_datetime = now()
        image.status = CONVERTED
    except Exception as e:
        image.status = FAILED
        image.issues = str(e)
    finally:
        image.job_id = ""
        image.save()

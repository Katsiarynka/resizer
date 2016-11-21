from django.utils.timezone import now
from PIL import Image as PilImage

from images.models import Image, FAILED, CONVERTED, DIR_CONVERTED
from resizer.celery import app
from resizer.settings import MEDIA_ROOT
from resizer.utils import publish_in_ws

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
        publish_in_ws(image)
    except Exception as e:
        image.status = FAILED
        image.issues = str(e)
    finally:
        image.job_id = ""
        image.save()

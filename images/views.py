from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from models import Image
from resizer.celery import resize


class LoadImage(APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, filename):
        original = request.data['file']
        image = Image.objects.create(original=original)
        job = resize.delay(image.id)
        image.job_id = job.id
        image.save(update_fields=['job_id'])
        return Response({"id": image.id})


class GetResizedImage(APIView):

    def get(self, request, pk):
        image = Image.objects.filter(id=pk).first()
        if not image:
            ValidationError({"error": "Image with {0} id not exists".format(pk)})

        converted_image = image.converted_image.load()
        return Response({"converted_image": converted_image})

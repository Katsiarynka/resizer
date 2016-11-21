from django.http import HttpResponseRedirect
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from models import Image
from resizer.settings import MEDIA_URL, MEDIA_ROOT
from .serializers import ImageSerializer


class ImageViewSet(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class GetResizedImage(APIView):

    def get(self, request, pk):
        image = Image.objects.filter(id=pk).first()
        if not image:
            raise ValidationError({"error": "Image with {0} id not exists".format(pk)})
        if not image.converted_image.name:
            raise ValidationError({"error": "Image hasn't converted yet".format(pk)})
        return HttpResponseRedirect(MEDIA_URL + image.converted_image.name.split(MEDIA_ROOT)[1])

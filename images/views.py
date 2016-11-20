from rest_framework.decorators import detail_route, parser_classes
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from models import Image, LOADED
from .tasks import resize
from .serializers import ImageSerializer


class ImageViewSet(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def perform_create(self, serializer):
        serializer.save(original=self.request.FILES.get('original'))


class GetResizedImage(APIView):

    def get(self, request, pk):
        image = Image.objects.filter(id=pk).first()
        if not image:
            ValidationError({"error": "Image with {0} id not exists".format(pk)})

        converted_image = image.converted_image.load()
        return Response({"converted_image": converted_image})

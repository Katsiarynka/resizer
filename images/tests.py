# tests.py
import os
from urlparse import urlparse

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from images.models import Image
from resizer import settings


class FileUploadTests(APITestCase):

    def setUp(self):
        self.tearDown()
        self.client = APIClient()
        self.url_image_list = reverse('image-list')
        self.dir_path = os.path.dirname(os.path.realpath(__file__))

    def tearDown(self):
        Image.objects.all().delete()

    def test_upload_jpg(self):
        data = dict()
        data['original_image'] = open(self.dir_path + '/test_data/1.jpg', 'rb')
        response = self.client.post(self.url_image_list, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('created', response.data)
        self.assertTrue(response.data['original_url'].startswith(settings.MEDIA_ROOT))
        self.assertIn('created', response.data)

    def test_upload_png(self):
        data = dict()
        data['original_image'] = open(self.dir_path + '/test_data/1.png', 'rb')
        response = self.client.post(self.url_image_list, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('created', response.data)
        self.assertTrue(response.data['original_url'].startswith(settings.MEDIA_ROOT))
        self.assertIn('created', response.data)

    def test_upload_png_like_jpg(self):
        data = dict()
        data['original_image'] = open(self.dir_path + '/test_data/1_png.jpg', 'rb')
        response = self.client.post(self.url_image_list, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('created', response.data)
        self.assertTrue(response.data['original_url'].startswith(settings.MEDIA_ROOT))
        self.assertIn('created', response.data)

    def test_upload_text_like_jpg(self):
        data = dict()
        data['original_image'] = open(self.dir_path + '/test_data/text.jpg', 'rb')
        response = self.client.post(self.url_image_list, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('original_image', response.data)

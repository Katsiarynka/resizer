# -*- coding: utf-8 -*-
import json
import os
import time
import requests

from django.test import LiveServerTestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from websocket import create_connection
from ws4redis.django_runserver import application


class WebsocketTests(LiveServerTestCase):
    fixtures = ['data.json']

    @classmethod
    def setUpClass(cls):
        os.environ.update(DJANGO_LIVE_TEST_SERVER_ADDRESS="localhost:8000-8010,8080,9200-9300")
        super(WebsocketTests, cls).setUpClass()
        cls.server_thread.httpd.set_app(application)

    def setUp(self):
        self.client = APIClient()
        self.url_image_list = reverse('image-list')
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        ws_base_url = self.live_server_url.replace('http:', 'ws:', 1) + u'/ws/foobar'
        ws_url = ws_base_url + u'?subscribe-broadcast&publish-broadcast&echo'
        self.ws = create_connection(ws_url)

    @classmethod
    def tearDownClass(cls):
        time.sleep(1)

    def tearDown(self):
        self.ws.close()

    def test_load_image(self):
        self.assertTrue(self.ws.connected)
        data = dict()
        data['original_image'] = open(self.dir_path + '/test_data/1.jpg', 'rb')
        self.client.post(self.url_image_list, data, format='multipart')
        result = json.loads(self.ws.recv())
        self.assertIn('id', result)
        self.assertIn('created', result)
        self.assertIn('converted_datetime', result)

    def test_invalid_request(self):
        incorrect_url = self.live_server_url.replace('http:', 'ws:', 1) + u'/ws/incorrect_url'
        self.assertRaises(Exception, requests.get, incorrect_url)

from django.conf.urls import url

from .views import LoadImage, GetResizedImage

urlpatterns = [
    url(r'^upload/(?P<filename>[^/]+)$', LoadImage.as_view()),
    url(r'^(?P<id>[a-z,0-9,-]+)/$', GetResizedImage.as_view()),
]

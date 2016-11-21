from django.conf.urls import url

from .views import GetResizedImage

urlpatterns = [
    url(r'^converted/(?P<pk>[0-9]+)/$', GetResizedImage.as_view()),
]

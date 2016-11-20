from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from images.views import ImageViewSet
from resizer import settings

router = DefaultRouter()
router.register(r'images', ImageViewSet)

urlpatterns = [
    url(r'^images/', include('images.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^static/media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
]

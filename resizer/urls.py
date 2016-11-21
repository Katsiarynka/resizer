from django.conf.urls import url, include
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from resizer import settings
from images.views import ImageViewSet

router = DefaultRouter()
router.register(r'images', ImageViewSet)

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html"), ),
    url(r'^api/', include(router.urls)),
    url(r'^images/', include('images.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

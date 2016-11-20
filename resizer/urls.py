from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/images/', include('images.urls')),
]

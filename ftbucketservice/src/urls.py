from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ImageViewSet


urlpatterns = [
    path('image', ImageViewSet.as_view({'post': 'create'})),
    path('image/serve', ImageViewSet.as_view({'get': 'image_serve'})),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

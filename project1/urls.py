
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

#handler404="project1.views.custom_page_not_found"

urlpatterns = [
    path('',include("blog.urls")),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

# Custom admin header and title
admin.site.site_header = "Dlyns Condo — Host Control Panel"
admin.site.site_title = "Dlyns Condo Admin"
admin.site.index_title = "Reservation Inquiries & Property Management"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('property_app.urls')),
    # Ensure uploaded room photos and media files are served in Docker/Dokploy
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

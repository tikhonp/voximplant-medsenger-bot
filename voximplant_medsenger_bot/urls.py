from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'Voximplant-Medsenger'
admin.site.site_title = 'Voximplant-Medsenger integration'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('medsenger/', include('medsenger_agent.urls')),
    path('forms/', include('forms.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

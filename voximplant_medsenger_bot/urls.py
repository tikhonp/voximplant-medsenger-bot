from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include

admin.site.site_header = 'Voximplant-Medsenger'
admin.site.site_title = 'Voximplant-Medsenger integration'

urlpatterns = [
    path('', lambda _: HttpResponse("Купил мужик шляпу, а она ему как раз! <a href=\"admin/\">🐔</a>")),
    path('admin/', admin.site.urls),
    path('medsenger/', include('medsenger_agent.urls')),
    path('forms/', include('forms.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

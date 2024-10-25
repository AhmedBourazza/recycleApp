# recyclingApplication/urls.py
from django.contrib import admin
from django.urls import path, include  # Ajoutez include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('myapp/', include('myapp.urls')),  # Inclure les URL de l'application
]

# Configuration pour servir des fichiers médias en mode développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
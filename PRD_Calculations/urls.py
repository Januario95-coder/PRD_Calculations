from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('prd/', include('webapp.urls', namespace='webapp')),
    path('api/', include('webapp.api.urls', namespace='status_api')),
    path('api-auth/', include('rest_framework.urls')),
]

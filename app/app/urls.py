from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # API schema, docs

    # Generates schema file (YAML)
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    # feed the schema file to swagger to view the documentation
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'),
         name='api-docs'),

    # user API
    path('api/user/', include('user.urls')),
]

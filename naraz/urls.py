from django.contrib import admin
from django.urls import path, include

from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.conf import settings

#
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("account/", include("account.urls")),
    path("shop/", include("shop.urls")),
    path("cart/", include("cart.urls")),
    path('products/', include('products.urls')),
    path("api-auth/", include("rest_framework.urls")),
    # 1. Endpoint to retrieve the OpenAPI Schema (JSON/YAML)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # 2. Swagger UI endpoint (Interactive testing interface)
    path(
        'api/schema/swagger-ui/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    # 3. Optional: ReDoc UI endpoint (Readable documentation interface)
    path(
        'api/schema/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

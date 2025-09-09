"""
URL configuration for cfrm project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

@api_view(['GET'])
@permission_classes([AllowAny])
def test_view(request):
    return Response({'message': 'Test OK'})

schema_view = get_schema_view(
    openapi.Info(
        title="CFRM API",
        default_version='v1',
        description="API pour la plateforme de feedback communautaire",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@cfrm.org"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('tickets.urls')),
    path('api/v1/', include('users.urls')),
    path('api/v1/', include('channels.urls')),
    path('api/v1/', include('analytics.urls')),
    path('api/v1/reports/', include('reports.urls')),
    # JWT Auth endpoints
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Test endpoint
    path('api/v1/test/', test_view, name='test'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

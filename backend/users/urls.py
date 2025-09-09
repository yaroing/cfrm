"""
URLs pour l'API des utilisateurs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'organizations', views.OrganizationViewSet)
router.register(r'roles', views.RoleViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'preferences', views.UserPreferenceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Auth alias endpoints
    path('auth/login/', views.AuthLoginView.as_view(), name='auth-login'),
    path('auth/logout/', views.UserViewSet.as_view({'post': 'logout'}), name='auth-logout'),
    path('auth/me/', views.UserViewSet.as_view({'get': 'me'}), name='auth-me'),
]

"""
URLs pour l'API Analytics
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'report-templates', views.ReportTemplateViewSet)
router.register(r'reports', views.ReportViewSet)
router.register(r'dashboards', views.DashboardViewSet)
router.register(r'widgets', views.WidgetViewSet)
router.register(r'metrics', views.MetricViewSet)
router.register(r'metric-values', views.MetricValueViewSet)
router.register(r'alerts', views.AlertViewSet)
router.register(r'alert-events', views.AlertEventViewSet)
router.register(r'exports', views.ExportJobViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

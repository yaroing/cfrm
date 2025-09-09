"""
Vues pour l'API Analytics
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg, Count
from django.utils import timezone
from datetime import timedelta

from .models import (
    ReportTemplate, Report, Dashboard, Widget,
    Metric, MetricValue, Alert, AlertEvent, ExportJob
)
from .serializers import (
    ReportTemplateSerializer, ReportSerializer, DashboardSerializer, WidgetSerializer,
    MetricSerializer, MetricValueSerializer, AlertSerializer, AlertEventSerializer,
    ExportJobSerializer
)


class ReportTemplateViewSet(viewsets.ModelViewSet):
    queryset = ReportTemplate.objects.all()
    serializer_class = ReportTemplateSerializer
    permission_classes = [IsAuthenticated]


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def recent(self, request):
        qs = self.get_queryset().order_by('-created_at')[:10]
        return Response(ReportSerializer(qs, many=True).data)


class DashboardViewSet(viewsets.ModelViewSet):
    queryset = Dashboard.objects.all()
    serializer_class = DashboardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        # Optionally filter to public or owned dashboards
        return qs.filter(is_public=True) | qs.filter(created_by=self.request.user)


class WidgetViewSet(viewsets.ModelViewSet):
    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer
    permission_classes = [IsAuthenticated]


class MetricViewSet(viewsets.ModelViewSet):
    queryset = Metric.objects.all()
    serializer_class = MetricSerializer
    permission_classes = [IsAuthenticated]


class MetricValueViewSet(viewsets.ModelViewSet):
    queryset = MetricValue.objects.all()
    serializer_class = MetricValueSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Summary over the last 7 days for a metric (by id query param)"""
        metric_id = request.query_params.get('metric')
        if not metric_id:
            return Response({'error': 'metric query param required'}, status=status.HTTP_400_BAD_REQUEST)
        end = timezone.now()
        start = end - timedelta(days=7)
        qs = MetricValue.objects.filter(metric_id=metric_id, timestamp__gte=start, timestamp__lte=end)
        data = {
            'count': qs.count(),
            'avg': qs.aggregate(v=Avg('value'))['v'],
        }
        return Response(data)


class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]


class AlertEventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AlertEvent.objects.all()
    serializer_class = AlertEventSerializer
    permission_classes = [IsAuthenticated]


class ExportJobViewSet(viewsets.ModelViewSet):
    queryset = ExportJob.objects.all()
    serializer_class = ExportJobSerializer
    permission_classes = [IsAuthenticated]

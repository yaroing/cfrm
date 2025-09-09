"""
Sérialiseurs pour l'API Analytics
"""
from rest_framework import serializers
from .models import (
    ReportTemplate, Report, Dashboard, Widget,
    Metric, MetricValue, Alert, AlertEvent, ExportJob
)


class ReportTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportTemplate
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'generated_at', 'status', 'error_message']


class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class MetricValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetricValue
        fields = '__all__'


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'last_triggered', 'trigger_count']


class AlertEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertEvent
        fields = '__all__'
        read_only_fields = ['triggered_at']


class ExportJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExportJob
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'completed_at', 'status', 'file_path', 'file_size', 'error_message']

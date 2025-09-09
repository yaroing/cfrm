"""
Modèles pour l'analytics et les rapports
"""
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class ReportTemplate(models.Model):
    """Modèles de rapports prédéfinis"""
    REPORT_TYPES = [
        ('tickets_summary', 'Résumé des tickets'),
        ('performance_metrics', 'Métriques de performance'),
        ('channel_analysis', 'Analyse des canaux'),
        ('user_activity', 'Activité des utilisateurs'),
        ('psea_analysis', 'Analyse PSEA'),
        ('custom', 'Rapport personnalisé'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    
    # Configuration du rapport
    query_filters = models.JSONField(default=dict, help_text="Filtres de base pour le rapport")
    chart_config = models.JSONField(default=dict, help_text="Configuration des graphiques")
    export_formats = models.JSONField(default=list, help_text="Formats d'export supportés")
    
    # Métadonnées
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=False, help_text="Visible par tous les utilisateurs")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_reports')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Modèle de rapport"
        verbose_name_plural = "Modèles de rapports"
        ordering = ['name']

    def __str__(self):
        return self.name


class Report(models.Model):
    """Rapports générés"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Informations de base
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    template = models.ForeignKey(ReportTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Paramètres du rapport
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    filters = models.JSONField(default=dict)
    
    # Données du rapport
    data = models.JSONField(default=dict)
    charts = models.JSONField(default=list)
    
    # Métadonnées
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports')
    created_at = models.DateTimeField(auto_now_add=True)
    generated_at = models.DateTimeField(null=True, blank=True)
    file_path = models.CharField(max_length=500, blank=True)
    
    # Statut
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('generating', 'Génération en cours'),
        ('completed', 'Terminé'),
        ('failed', 'Échec'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)

    class Meta:
        verbose_name = "Rapport"
        verbose_name_plural = "Rapports"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d')}"


class Dashboard(models.Model):
    """Tableaux de bord personnalisés"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Configuration du tableau de bord
    layout = models.JSONField(default=dict)
    widgets = models.JSONField(default=list)
    filters = models.JSONField(default=dict)
    
    # Métadonnées
    is_public = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dashboards')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tableau de bord"
        verbose_name_plural = "Tableaux de bord"
        ordering = ['name']

    def __str__(self):
        return self.name


class Widget(models.Model):
    """Widgets pour les tableaux de bord"""
    WIDGET_TYPES = [
        ('chart', 'Graphique'),
        ('metric', 'Métrique'),
        ('table', 'Tableau'),
        ('list', 'Liste'),
        ('map', 'Carte'),
        ('text', 'Texte'),
    ]
    
    name = models.CharField(max_length=200)
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPES)
    description = models.TextField(blank=True)
    
    # Configuration du widget
    config = models.JSONField(default=dict)
    query = models.JSONField(default=dict)
    
    # Métadonnées
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='widgets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Widget"
        verbose_name_plural = "Widgets"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_widget_type_display()})"


class Metric(models.Model):
    """Métriques de performance"""
    METRIC_TYPES = [
        ('counter', 'Compteur'),
        ('gauge', 'Jauge'),
        ('histogram', 'Histogramme'),
        ('rate', 'Taux'),
    ]
    
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    metric_type = models.CharField(max_length=20, choices=METRIC_TYPES)
    
    # Configuration de la métrique
    query = models.JSONField(default=dict)
    unit = models.CharField(max_length=20, blank=True)
    target_value = models.FloatField(null=True, blank=True)
    warning_threshold = models.FloatField(null=True, blank=True)
    critical_threshold = models.FloatField(null=True, blank=True)
    
    # Métadonnées
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Métrique"
        verbose_name_plural = "Métriques"
        ordering = ['name']

    def __str__(self):
        return self.name


class MetricValue(models.Model):
    """Valeurs des métriques dans le temps"""
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE, related_name='values')
    value = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)
    
    # Métadonnées contextuelles
    context = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = "Valeur de métrique"
        verbose_name_plural = "Valeurs de métriques"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['metric', 'timestamp']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.metric.name}: {self.value} @ {self.timestamp}"


class Alert(models.Model):
    """Alertes basées sur les métriques"""
    SEVERITY_CHOICES = [
        ('low', 'Faible'),
        ('medium', 'Moyen'),
        ('high', 'Élevé'),
        ('critical', 'Critique'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE, related_name='alerts')
    
    # Conditions d'alerte
    condition = models.JSONField(default=dict)
    threshold = models.FloatField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='medium')
    
    # Configuration des notifications
    notification_channels = models.JSONField(default=list)
    notification_template = models.TextField(blank=True)
    
    # Statut
    is_active = models.BooleanField(default=True)
    last_triggered = models.DateTimeField(null=True, blank=True)
    trigger_count = models.IntegerField(default=0)
    
    # Métadonnées
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='alerts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Alerte"
        verbose_name_plural = "Alertes"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.get_severity_display()}"


class AlertEvent(models.Model):
    """Événements d'alerte déclenchés"""
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='events')
    metric_value = models.ForeignKey(MetricValue, on_delete=models.CASCADE, related_name='alert_events')
    
    # Informations de l'événement
    triggered_at = models.DateTimeField(default=timezone.now)
    value = models.FloatField()
    threshold = models.FloatField()
    message = models.TextField()
    
    # Statut de notification
    notifications_sent = models.BooleanField(default=False)
    notifications_sent_at = models.DateTimeField(null=True, blank=True)
    
    # Résolution
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    resolution_notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Événement d'alerte"
        verbose_name_plural = "Événements d'alerte"
        ordering = ['-triggered_at']

    def __str__(self):
        return f"Alerte {self.alert.name} - {self.triggered_at}"


class ExportJob(models.Model):
    """Tâches d'export de données"""
    EXPORT_FORMATS = [
        ('csv', 'CSV'),
        ('excel', 'Excel'),
        ('pdf', 'PDF'),
        ('json', 'JSON'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Informations de base
    name = models.CharField(max_length=200)
    export_format = models.CharField(max_length=20, choices=EXPORT_FORMATS)
    
    # Paramètres d'export
    query_filters = models.JSONField(default=dict)
    fields = models.JSONField(default=list)
    date_range = models.JSONField(default=dict)
    
    # Statut
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('processing', 'Traitement en cours'),
        ('completed', 'Terminé'),
        ('failed', 'Échec'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Résultat
    file_path = models.CharField(max_length=500, blank=True)
    file_size = models.BigIntegerField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    
    # Métadonnées
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='export_jobs')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Tâche d'export"
        verbose_name_plural = "Tâches d'export"
        ordering = ['-created_at']

    def __str__(self):
        return f"Export {self.name} - {self.get_export_format_display()}"

"""
Modèles pour la gestion des utilisateurs et des rôles
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid


class Organization(models.Model):
    """Organisations (ONG, agences, etc.)"""
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Organisation"
        verbose_name_plural = "Organisations"
        ordering = ['name']

    def __str__(self):
        return self.name


class Role(models.Model):
    """Rôles des utilisateurs dans le système"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    permissions = models.JSONField(default=list, help_text="Liste des permissions")
    is_psea_authorized = models.BooleanField(default=False, help_text="Accès aux cas PSEA")
    can_escalate = models.BooleanField(default=False, help_text="Peut escalader des tickets")
    can_assign = models.BooleanField(default=False, help_text="Peut assigner des tickets")
    can_close = models.BooleanField(default=False, help_text="Peut fermer des tickets")
    can_view_analytics = models.BooleanField(default=False, help_text="Accès aux analytics")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Rôle"
        verbose_name_plural = "Rôles"
        ordering = ['name']

    def __str__(self):
        return self.name


class User(AbstractUser):
    """Utilisateur étendu avec informations supplémentaires"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Informations personnelles
    phone = models.CharField(max_length=20, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True, blank=True)
    
    # Informations de localisation
    location = models.CharField(max_length=200, blank=True)
    timezone = models.CharField(max_length=50, default='UTC')
    language = models.CharField(max_length=10, default='fr')
    
    # Statut et préférences
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_activity = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"

    @property
    def full_name(self):
        return self.get_full_name() or self.username

    def has_permission(self, permission):
        """Vérifier si l'utilisateur a une permission spécifique"""
        if self.is_superuser:
            return True
        if self.role:
            return permission in self.role.permissions
        return False

    def can_access_psea(self):
        """Vérifier si l'utilisateur peut accéder aux cas PSEA"""
        return self.is_superuser or (self.role and self.role.is_psea_authorized)

    def update_last_activity(self):
        """Mettre à jour la dernière activité"""
        self.last_activity = timezone.now()
        self.save(update_fields=['last_activity'])


class UserSession(models.Model):
    """Sessions utilisateur pour le suivi"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Session utilisateur"
        verbose_name_plural = "Sessions utilisateur"
        ordering = ['-last_activity']

    def __str__(self):
        return f"Session {self.user.username} - {self.created_at}"


class UserActivity(models.Model):
    """Journal des activités utilisateur"""
    ACTION_TYPES = [
        ('login', 'Connexion'),
        ('logout', 'Déconnexion'),
        ('ticket_view', 'Consultation ticket'),
        ('ticket_create', 'Création ticket'),
        ('ticket_update', 'Modification ticket'),
        ('ticket_assign', 'Assignation ticket'),
        ('ticket_close', 'Fermeture ticket'),
        ('response_create', 'Création réponse'),
        ('analytics_view', 'Consultation analytics'),
        ('admin_access', 'Accès administration'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=50, choices=ACTION_TYPES)
    description = models.TextField()
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Activité utilisateur"
        verbose_name_plural = "Activités utilisateur"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'action']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.get_action_display()}"


class UserPreference(models.Model):
    """Préférences utilisateur"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    
    # Préférences d'interface
    theme = models.CharField(max_length=20, default='light', choices=[
        ('light', 'Clair'),
        ('dark', 'Sombre'),
        ('auto', 'Automatique'),
    ])
    items_per_page = models.IntegerField(default=20)
    default_view = models.CharField(max_length=50, default='list')
    
    # Notifications
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=True)
    
    # Filtres par défaut
    default_filters = models.JSONField(default=dict, blank=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Préférence utilisateur"
        verbose_name_plural = "Préférences utilisateur"

    def __str__(self):
        return f"Préférences de {self.user.username}"

"""
Modèles pour la gestion des tickets de feedback
"""
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class Category(models.Model):
    """Catégories de feedback (plainte, demande info, PEAS, etc.)"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_sensitive = models.BooleanField(default=False, help_text="Catégorie sensible (PSEA/SEA)")
    requires_escalation = models.BooleanField(default=False, help_text="Nécessite une escalade automatique")
    escalation_contact = models.EmailField(blank=True, help_text="Contact pour escalade")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Priority(models.Model):
    """Niveaux de priorité des tickets"""
    name = models.CharField(max_length=50, unique=True)
    level = models.IntegerField(unique=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    color = models.CharField(max_length=7, default="#000000", help_text="Couleur hexadécimale")
    sla_hours = models.IntegerField(help_text="SLA en heures")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Priorité"
        verbose_name_plural = "Priorités"
        ordering = ['level']

    def __str__(self):
        return f"{self.name} (Niveau {self.level})"


class Status(models.Model):
    """Statuts des tickets"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    is_final = models.BooleanField(default=False, help_text="Statut final (ferme le ticket)")
    color = models.CharField(max_length=7, default="#000000")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Statut"
        verbose_name_plural = "Statuts"
        ordering = ['name']

    def __str__(self):
        return self.name


class Channel(models.Model):
    """Canaux de collecte (SMS, WhatsApp, Web, etc.)"""
    CHANNEL_TYPES = [
        ('sms', 'SMS'),
        ('whatsapp', 'WhatsApp'),
        ('web', 'Web'),
        ('email', 'Email'),
        ('phone', 'Téléphone'),
        ('paper', 'Papier'),
        ('other', 'Autre'),
    ]

    name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=20, choices=CHANNEL_TYPES)
    is_active = models.BooleanField(default=True)
    configuration = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Canal"
        verbose_name_plural = "Canaux"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Ticket(models.Model):
    """Ticket de feedback principal"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Informations de base
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_anonymous = models.BooleanField(default=False)
    
    # Classification
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='tickets')
    priority = models.ForeignKey(Priority, on_delete=models.PROTECT, related_name='tickets')
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name='tickets')
    
    # Canal et origine
    channel = models.ForeignKey(Channel, on_delete=models.PROTECT, related_name='tickets')
    external_id = models.CharField(max_length=100, blank=True, help_text="ID externe (SMS, WhatsApp, etc.)")
    
    # Informations du plaignant (optionnelles si anonyme)
    submitter_name = models.CharField(max_length=100, blank=True)
    submitter_phone = models.CharField(max_length=20, blank=True)
    submitter_email = models.EmailField(blank=True)
    submitter_location = models.CharField(max_length=200, blank=True)
    
    # Assignation et suivi
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_tickets')
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    
    # SLA et escalade
    sla_deadline = models.DateTimeField(null=True, blank=True)
    escalated_at = models.DateTimeField(null=True, blank=True)
    escalated_to = models.EmailField(blank=True)
    
    # Données sensibles PSEA
    is_psea = models.BooleanField(default=False)
    psea_contact = models.EmailField(blank=True)
    psea_escalated = models.BooleanField(default=False)
    
    # Fichiers joints
    attachments = models.JSONField(default=list, blank=True)
    
    # Données de localisation
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Tags et métadonnées
    tags = models.JSONField(default=list, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'priority']),
            models.Index(fields=['category', 'is_psea']),
            models.Index(fields=['created_at']),
            models.Index(fields=['assigned_to']),
        ]

    def __str__(self):
        return f"#{self.id} - {self.title}"

    def save(self, *args, **kwargs):
        # Calculer le SLA si pas défini
        if not self.sla_deadline and self.priority:
            self.sla_deadline = timezone.now() + timezone.timedelta(hours=self.priority.sla_hours)
        
        # Marquer comme PSEA si la catégorie l'exige
        if self.category and self.category.is_sensitive:
            self.is_psea = True
        
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        """Vérifie si le ticket est en retard"""
        if not self.sla_deadline or self.status.is_final:
            return False
        return timezone.now() > self.sla_deadline

    @property
    def days_since_creation(self):
        """Nombre de jours depuis la création"""
        return (timezone.now() - self.created_at).days


class Response(models.Model):
    """Réponses aux tickets"""
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='responses')
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    channel = models.ForeignKey(Channel, on_delete=models.PROTECT, related_name='responses')
    is_internal = models.BooleanField(default=False, help_text="Note interne (non visible par le plaignant)")
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Métadonnées de l'envoi
    delivery_status = models.CharField(max_length=50, blank=True)
    external_message_id = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Réponse"
        verbose_name_plural = "Réponses"
        ordering = ['-created_at']

    def __str__(self):
        return f"Réponse pour #{self.ticket.id}"


class TicketLog(models.Model):
    """Journal des actions sur les tickets"""
    ACTION_TYPES = [
        ('created', 'Créé'),
        ('updated', 'Modifié'),
        ('assigned', 'Assigné'),
        ('status_changed', 'Statut modifié'),
        ('priority_changed', 'Priorité modifiée'),
        ('escalated', 'Escaladé'),
        ('closed', 'Fermé'),
        ('reopened', 'Rouvert'),
        ('response_added', 'Réponse ajoutée'),
    ]

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='logs')
    action = models.CharField(max_length=50, choices=ACTION_TYPES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    old_value = models.CharField(max_length=200, blank=True)
    new_value = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        verbose_name = "Log de ticket"
        verbose_name_plural = "Logs de tickets"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_action_display()} - #{self.ticket.id}"


class Feedback(models.Model):
    """Évaluation de satisfaction post-traitement"""
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, related_name='feedback')
    satisfaction_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Note de satisfaction de 1 à 5"
    )
    response_time_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Note du délai de réponse de 1 à 5"
    )
    quality_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Note de la qualité de la réponse de 1 à 5"
    )
    comments = models.TextField(blank=True)
    would_recommend = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"

    def __str__(self):
        return f"Feedback pour #{self.ticket.id} - {self.satisfaction_rating}/5"

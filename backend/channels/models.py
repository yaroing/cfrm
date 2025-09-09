"""
Modèles pour la gestion des canaux de communication
"""
from django.db import models
from django.utils import timezone
import uuid


class ChannelConfiguration(models.Model):
    """Configuration des canaux de communication"""
    CHANNEL_TYPES = [
        ('sms', 'SMS'),
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
        ('web', 'Web'),
        ('phone', 'Téléphone'),
        ('paper', 'Papier'),
        ('other', 'Autre'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=20, choices=CHANNEL_TYPES)
    is_active = models.BooleanField(default=True)
    
    # Configuration spécifique au canal
    configuration = models.JSONField(default=dict)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Configuration de canal"
        verbose_name_plural = "Configurations de canaux"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class MessageTemplate(models.Model):
    """Modèles de messages pour les différents canaux"""
    name = models.CharField(max_length=100)
    channel = models.ForeignKey(ChannelConfiguration, on_delete=models.CASCADE, related_name='templates')
    template_type = models.CharField(max_length=50, choices=[
        ('welcome', 'Message de bienvenue'),
        ('confirmation', 'Confirmation de réception'),
        ('response', 'Réponse standard'),
        ('escalation', 'Notification d\'escalade'),
        ('closure', 'Notification de fermeture'),
        ('reminder', 'Rappel'),
    ])
    
    # Contenu du template
    subject = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    language = models.CharField(max_length=10, default='fr')
    
    # Variables disponibles dans le template
    variables = models.JSONField(default=list, help_text="Liste des variables disponibles")
    
    # Statut
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Modèle de message"
        verbose_name_plural = "Modèles de messages"
        ordering = ['name']
        unique_together = ['name', 'channel', 'template_type', 'language']

    def __str__(self):
        return f"{self.name} - {self.get_template_type_display()}"


class Message(models.Model):
    """Messages envoyés via les différents canaux"""
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('sent', 'Envoyé'),
        ('delivered', 'Livré'),
        ('failed', 'Échec'),
        ('read', 'Lu'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Canal et destinataire
    channel = models.ForeignKey(ChannelConfiguration, on_delete=models.PROTECT)
    recipient = models.CharField(max_length=200, help_text="Numéro de téléphone, email, etc.")
    
    # Contenu
    subject = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    template = models.ForeignKey(MessageTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Statut et suivi
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    external_id = models.CharField(max_length=100, blank=True, help_text="ID du message dans le système externe")
    error_message = models.TextField(blank=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Liens
    ticket = models.ForeignKey('tickets.Ticket', on_delete=models.CASCADE, null=True, blank=True, related_name='messages')
    response = models.ForeignKey('tickets.Response', on_delete=models.CASCADE, null=True, blank=True, related_name='messages')
    
    # Métadonnées techniques
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['channel', 'recipient']),
            models.Index(fields=['ticket']),
        ]

    def __str__(self):
        return f"Message {self.id} - {self.channel.name} - {self.recipient}"

    def mark_as_sent(self, external_id=None):
        """Marquer le message comme envoyé"""
        self.status = 'sent'
        self.sent_at = timezone.now()
        if external_id:
            self.external_id = external_id
        self.save()

    def mark_as_delivered(self):
        """Marquer le message comme livré"""
        self.status = 'delivered'
        self.delivered_at = timezone.now()
        self.save()

    def mark_as_failed(self, error_message):
        """Marquer le message comme échoué"""
        self.status = 'failed'
        self.error_message = error_message
        self.save()

    def mark_as_read(self):
        """Marquer le message comme lu"""
        self.status = 'read'
        self.read_at = timezone.now()
        self.save()


class WebhookEvent(models.Model):
    """Événements webhook reçus des services externes"""
    EVENT_TYPES = [
        ('sms_received', 'SMS reçu'),
        ('whatsapp_received', 'WhatsApp reçu'),
        ('email_received', 'Email reçu'),
        ('delivery_status', 'Statut de livraison'),
        ('read_status', 'Statut de lecture'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    channel = models.ForeignKey(ChannelConfiguration, on_delete=models.PROTECT)
    
    # Données de l'événement
    payload = models.JSONField()
    headers = models.JSONField(default=dict)
    
    # Traitement
    processed = models.BooleanField(default=False)
    processed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    
    # Liens
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, blank=True)
    ticket = models.ForeignKey('tickets.Ticket', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    source_ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        verbose_name = "Événement webhook"
        verbose_name_plural = "Événements webhook"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['event_type', 'processed']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Webhook {self.event_type} - {self.created_at}"

    def mark_as_processed(self):
        """Marquer l'événement comme traité"""
        self.processed = True
        self.processed_at = timezone.now()
        self.save()

    def mark_as_failed(self, error_message):
        """Marquer l'événement comme échoué"""
        self.error_message = error_message
        self.save()


class ChannelStats(models.Model):
    """Statistiques des canaux"""
    channel = models.ForeignKey(ChannelConfiguration, on_delete=models.CASCADE, related_name='stats')
    date = models.DateField()
    
    # Compteurs
    messages_sent = models.IntegerField(default=0)
    messages_delivered = models.IntegerField(default=0)
    messages_failed = models.IntegerField(default=0)
    messages_read = models.IntegerField(default=0)
    
    # Métriques de performance
    avg_delivery_time = models.FloatField(null=True, blank=True, help_text="Temps de livraison moyen en secondes")
    success_rate = models.FloatField(null=True, blank=True, help_text="Taux de succès en pourcentage")
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Statistique de canal"
        verbose_name_plural = "Statistiques de canaux"
        ordering = ['-date']
        unique_together = ['channel', 'date']

    def __str__(self):
        return f"Stats {self.channel.name} - {self.date}"

    def calculate_metrics(self):
        """Calculer les métriques de performance"""
        total = self.messages_sent
        if total > 0:
            self.success_rate = (self.messages_delivered / total) * 100
        else:
            self.success_rate = 0
        self.save()

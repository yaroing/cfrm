"""
Sérialiseurs pour l'API des tickets
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.utils import timezone
from .models import (
    Category, Priority, Status, Channel, Ticket, 
    Response, TicketLog, Feedback
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        # Unique name for OpenAPI schema to avoid conflict with users.serializers.UserSerializer
        ref_name = 'TicketsUser'
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class TicketLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)

    class Meta:
        model = TicketLog
        fields = '__all__'


class ResponseSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    channel_name = serializers.CharField(source='channel.name', read_only=True)

    class Meta:
        model = Response
        fields = ['ticket', 'content', 'is_internal', 'author', 'channel_name', 'sent_at', 'delivery_status', 'external_message_id', 'created_at']
        read_only_fields = ['author', 'channel_name', 'sent_at', 'delivery_status', 'external_message_id', 'created_at']

    def create(self, validated_data):
        import logging
        logger = logging.getLogger(__name__)
        
        logger.info(f"ResponseSerializer.create called with data: {validated_data}")
        
        # Si aucun channel n'est fourni, utiliser le channel "Portail Web" par défaut
        if 'channel' not in validated_data:
            from .models import Channel
            web_channel = Channel.objects.filter(name='Portail Web').first()
            if web_channel:
                validated_data['channel'] = web_channel
                logger.info(f"Added default channel: {web_channel}")
            else:
                logger.error("Portail Web channel not found!")
        
        logger.info(f"Final validated_data: {validated_data}")
        return super().create(validated_data)


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    priority_name = serializers.CharField(source='priority.name', read_only=True)
    status_name = serializers.CharField(source='status.name', read_only=True)
    channel_name = serializers.CharField(source='channel.name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    days_since_creation = serializers.IntegerField(read_only=True)
    responses = ResponseSerializer(many=True, read_only=True)
    logs = TicketLogSerializer(many=True, read_only=True)
    feedback = FeedbackSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'closed_at']

    def create(self, validated_data):
        # Log de création
        # Extraire les fichiers avant la création
        uploaded_files = validated_data.pop('attachments', [])

        ticket = super().create(validated_data)

        # Sauvegarder les fichiers et renseigner ticket.attachments (liste de dicts)
        if uploaded_files:
            saved = []
            for f in uploaded_files:
                # Dossier par date pour éviter collisions
                path = default_storage.save(f"tickets/{timezone.now().date()}/{f.name}", f)
                saved.append({
                    'name': f.name,
                    'path': path,
                    'size': getattr(f, 'size', None),
                    'content_type': getattr(f, 'content_type', None),
                })
            ticket.attachments = saved
            ticket.save(update_fields=['attachments'])
        request = self.context.get('request')
        user = request.user if request and request.user.is_authenticated else None
        ip_address = request.META.get('REMOTE_ADDR') if request else None
        
        TicketLog.objects.create(
            ticket=ticket,
            action='created',
            user=user,
            description=f"Ticket créé via {ticket.channel.name}",
            ip_address=ip_address
        )
        return ticket


class TicketCreateSerializer(serializers.ModelSerializer):
    """Sérialiseur simplifié pour la création de tickets"""
    # Pièces jointes envoyées en multipart/form-data
    attachments = serializers.ListField(
        child=serializers.FileField(allow_empty_file=False),
        write_only=True,
        required=False
    )
    class Meta:
        model = Ticket
        fields = [
            'title', 'content', 'is_anonymous', 'category', 'priority',
            'channel', 'external_id', 'submitter_name', 'submitter_phone',
            'submitter_email', 'submitter_location', 'latitude', 'longitude',
            'tags', 'metadata', 'attachments'
        ]

    def create(self, validated_data):
        # Définir des valeurs par défaut
        if not validated_data.get('priority'):
            validated_data['priority'] = Priority.objects.filter(level=3).first()
        
        if not validated_data.get('status'):
            validated_data['status'] = Status.objects.filter(name='Ouvert').first()

        ticket = super().create(validated_data)
        
        # Log de création
        request = self.context.get('request')
        user = request.user if request and request.user.is_authenticated else None
        ip_address = request.META.get('REMOTE_ADDR') if request else None
        
        TicketLog.objects.create(
            ticket=ticket,
            action='created',
            user=user,
            description=f"Ticket créé via {ticket.channel.name}",
            ip_address=ip_address
        )
        
        return ticket


class TicketUpdateSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la mise à jour des tickets"""
    class Meta:
        model = Ticket
        fields = [
            'title', 'content', 'category', 'priority', 'status',
            'assigned_to', 'submitter_name', 'submitter_phone',
            'submitter_email', 'submitter_location', 'latitude',
            'longitude', 'tags', 'metadata'
        ]

    def update(self, instance, validated_data):
        old_status = instance.status
        old_priority = instance.priority
        old_assigned = instance.assigned_to
        
        ticket = super().update(instance, validated_data)
        
        # Log des changements
        request = self.context.get('request')
        user = request.user if request and request.user.is_authenticated else None
        ip_address = request.META.get('REMOTE_ADDR') if request else None
        
        if old_status != ticket.status:
            TicketLog.objects.create(
                ticket=ticket,
                action='status_changed',
                user=user,
                description=f"Statut changé de {old_status} à {ticket.status}",
                old_value=str(old_status),
                new_value=str(ticket.status),
                ip_address=ip_address
            )
        
        if old_priority != ticket.priority:
            TicketLog.objects.create(
                ticket=ticket,
                action='priority_changed',
                user=user,
                description=f"Priorité changée de {old_priority} à {ticket.priority}",
                old_value=str(old_priority),
                new_value=str(ticket.priority),
                ip_address=ip_address
            )
        
        if old_assigned != ticket.assigned_to:
            TicketLog.objects.create(
                ticket=ticket,
                action='assigned',
                user=user,
                description=f"Ticket assigné à {ticket.assigned_to or 'Personne'}",
                old_value=str(old_assigned) if old_assigned else '',
                new_value=str(ticket.assigned_to) if ticket.assigned_to else '',
                ip_address=ip_address
            )
        
        return ticket

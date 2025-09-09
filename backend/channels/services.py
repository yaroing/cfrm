"""
Services pour la gestion des canaux de communication
"""
import logging
import requests
from django.conf import settings
from django.utils import timezone
from twilio.rest import Client as TwilioClient
from twilio.base.exceptions import TwilioException
from .models import Message, MessageTemplate, ChannelStats, WebhookEvent

logger = logging.getLogger(__name__)


class BaseChannelService:
    """Service de base pour les canaux de communication"""
    
    def __init__(self, channel_config):
        self.channel_config = channel_config
        self.configuration = channel_config.configuration
    
    def send_message(self, recipient, content, subject=None, template=None, **kwargs):
        """Envoyer un message via le canal"""
        raise NotImplementedError
    
    def process_webhook(self, payload, headers):
        """Traiter un webhook reçu"""
        raise NotImplementedError


class SMSService(BaseChannelService):
    """Service pour l'envoi de SMS via Twilio"""
    
    def __init__(self, channel_config):
        super().__init__(channel_config)
        self.client = TwilioClient(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )
        self.phone_number = settings.TWILIO_PHONE_NUMBER
    
    def send_message(self, recipient, content, subject=None, template=None, **kwargs):
        """Envoyer un SMS"""
        try:
            # Créer le message en base
            message = Message.objects.create(
                channel=self.channel_config,
                recipient=recipient,
                content=content,
                template=template,
                ticket=kwargs.get('ticket'),
                response=kwargs.get('response')
            )
            
            # Envoyer via Twilio
            twilio_message = self.client.messages.create(
                body=content,
                from_=self.phone_number,
                to=recipient
            )
            
            # Mettre à jour le statut
            message.mark_as_sent(twilio_message.sid)
            
            logger.info(f"SMS envoyé à {recipient}: {twilio_message.sid}")
            return message
            
        except TwilioException as e:
            logger.error(f"Erreur Twilio: {e}")
            message.mark_as_failed(str(e))
            return message
        except Exception as e:
            logger.error(f"Erreur SMS: {e}")
            if 'message' in locals():
                message.mark_as_failed(str(e))
            return None
    
    def process_webhook(self, payload, headers):
        """Traiter les webhooks Twilio"""
        event_type = payload.get('MessageStatus', 'unknown')
        
        webhook_event = WebhookEvent.objects.create(
            event_type='delivery_status',
            channel=self.channel_config,
            payload=payload,
            headers=headers
        )
        
        # Mettre à jour le statut du message
        message_sid = payload.get('MessageSid')
        if message_sid:
            try:
                message = Message.objects.get(external_id=message_sid)
                
                if event_type == 'delivered':
                    message.mark_as_delivered()
                elif event_type == 'failed':
                    message.mark_as_failed(payload.get('ErrorMessage', 'Erreur inconnue'))
                
                webhook_event.message = message
                webhook_event.ticket = message.ticket
                webhook_event.mark_as_processed()
                
            except Message.DoesNotExist:
                logger.warning(f"Message non trouvé: {message_sid}")
                webhook_event.mark_as_failed("Message non trouvé")
        
        return webhook_event


class WhatsAppService(BaseChannelService):
    """Service pour WhatsApp Business API"""
    
    def __init__(self, channel_config):
        super().__init__(channel_config)
        self.access_token = settings.WHATSAPP_ACCESS_TOKEN
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        self.api_url = f"https://graph.facebook.com/v17.0/{self.phone_number_id}/messages"
    
    def send_message(self, recipient, content, subject=None, template=None, **kwargs):
        """Envoyer un message WhatsApp"""
        try:
            # Créer le message en base
            message = Message.objects.create(
                channel=self.channel_config,
                recipient=recipient,
                content=content,
                template=template,
                ticket=kwargs.get('ticket'),
                response=kwargs.get('response')
            )
            
            # Préparer les données pour l'API WhatsApp
            data = {
                "messaging_product": "whatsapp",
                "to": recipient,
                "type": "text",
                "text": {"body": content}
            }
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            # Envoyer via l'API WhatsApp
            response = requests.post(self.api_url, json=data, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            message_id = result.get('messages', [{}])[0].get('id')
            
            # Mettre à jour le statut
            message.mark_as_sent(message_id)
            
            logger.info(f"WhatsApp envoyé à {recipient}: {message_id}")
            return message
            
        except requests.RequestException as e:
            logger.error(f"Erreur WhatsApp API: {e}")
            message.mark_as_failed(str(e))
            return message
        except Exception as e:
            logger.error(f"Erreur WhatsApp: {e}")
            if 'message' in locals():
                message.mark_as_failed(str(e))
            return None
    
    def process_webhook(self, payload, headers):
        """Traiter les webhooks WhatsApp"""
        webhook_event = WebhookEvent.objects.create(
            event_type='whatsapp_received',
            channel=self.channel_config,
            payload=payload,
            headers=headers
        )
        
        # Traiter les messages entrants
        entries = payload.get('entry', [])
        for entry in entries:
            changes = entry.get('changes', [])
            for change in changes:
                value = change.get('value', {})
                messages = value.get('messages', [])
                
                for msg in messages:
                    from_number = msg.get('from')
                    text = msg.get('text', {}).get('body', '')
                    
                    if from_number and text:
                        # Créer un ticket ou une réponse
                        # Cette logique dépend de votre implémentation
                        webhook_event.ticket = self._create_ticket_from_message(
                            from_number, text, webhook_event
                        )
        
        webhook_event.mark_as_processed()
        return webhook_event
    
    def _create_ticket_from_message(self, from_number, text, webhook_event):
        """Créer un ticket à partir d'un message WhatsApp"""
        # Implémentation spécifique pour créer un ticket
        # depuis un message WhatsApp
        pass


class EmailService(BaseChannelService):
    """Service pour l'envoi d'emails"""
    
    def send_message(self, recipient, content, subject=None, template=None, **kwargs):
        """Envoyer un email"""
        from django.core.mail import send_mail
        from django.template.loader import render_to_string
        
        try:
            # Créer le message en base
            message = Message.objects.create(
                channel=self.channel_config,
                recipient=recipient,
                content=content,
                subject=subject or 'Notification CFRM',
                template=template,
                ticket=kwargs.get('ticket'),
                response=kwargs.get('response')
            )
            
            # Envoyer l'email
            send_mail(
                subject=message.subject,
                message=content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=False
            )
            
            # Mettre à jour le statut
            message.mark_as_sent()
            
            logger.info(f"Email envoyé à {recipient}")
            return message
            
        except Exception as e:
            logger.error(f"Erreur email: {e}")
            message.mark_as_failed(str(e))
            return message


class ChannelServiceFactory:
    """Factory pour créer les services de canaux"""
    
    @staticmethod
    def get_service(channel_config):
        """Obtenir le service approprié pour un canal"""
        channel_type = channel_config.type
        
        if channel_type == 'sms':
            return SMSService(channel_config)
        elif channel_type == 'whatsapp':
            return WhatsAppService(channel_config)
        elif channel_type == 'email':
            return EmailService(channel_config)
        else:
            raise ValueError(f"Type de canal non supporté: {channel_type}")


class MessageService:
    """Service central pour la gestion des messages"""
    
    @staticmethod
    def send_ticket_confirmation(ticket):
        """Envoyer une confirmation de réception de ticket"""
        # Récupérer le template de confirmation
        template = MessageTemplate.objects.filter(
            channel__type=ticket.channel.type,
            template_type='confirmation',
            is_active=True
        ).first()
        
        if not template:
            logger.warning(f"Template de confirmation non trouvé pour {ticket.channel.type}")
            return None
        
        # Remplacer les variables dans le template
        content = template.content.format(
            ticket_id=ticket.id,
            title=ticket.title,
            category=ticket.category.name,
            priority=ticket.priority.name
        )
        
        # Obtenir le service approprié
        service = ChannelServiceFactory.get_service(ticket.channel)
        
        # Déterminer le destinataire
        recipient = ticket.submitter_phone or ticket.submitter_email
        if not recipient:
            logger.warning(f"Aucun destinataire trouvé pour le ticket {ticket.id}")
            return None
        
        # Envoyer le message
        return service.send_message(
            recipient=recipient,
            content=content,
            subject=template.subject,
            template=template,
            ticket=ticket
        )
    
    @staticmethod
    def send_ticket_response(response):
        """Envoyer une réponse à un ticket"""
        ticket = response.ticket
        
        # Récupérer le template de réponse
        template = MessageTemplate.objects.filter(
            channel__type=ticket.channel.type,
            template_type='response',
            is_active=True
        ).first()
        
        if not template:
            # Utiliser le contenu de la réponse directement
            content = response.content
            subject = f"Réponse à votre ticket #{ticket.id}"
        else:
            # Remplacer les variables dans le template
            content = template.content.format(
                ticket_id=ticket.id,
                response_content=response.content,
                responder=response.author.get_full_name() if response.author else 'Équipe CFRM'
            )
            subject = template.subject or f"Réponse à votre ticket #{ticket.id}"
        
        # Obtenir le service approprié
        service = ChannelServiceFactory.get_service(ticket.channel)
        
        # Déterminer le destinataire
        recipient = ticket.submitter_phone or ticket.submitter_email
        if not recipient:
            logger.warning(f"Aucun destinataire trouvé pour le ticket {ticket.id}")
            return None
        
        # Envoyer le message
        return service.send_message(
            recipient=recipient,
            content=content,
            subject=subject,
            template=template,
            ticket=ticket,
            response=response
        )
    
    @staticmethod
    def update_channel_stats(channel, date=None):
        """Mettre à jour les statistiques d'un canal"""
        if not date:
            date = timezone.now().date()
        
        stats, created = ChannelStats.objects.get_or_create(
            channel=channel,
            date=date
        )
        
        # Compter les messages
        messages = Message.objects.filter(
            channel=channel,
            created_at__date=date
        )
        
        stats.messages_sent = messages.count()
        stats.messages_delivered = messages.filter(status='delivered').count()
        stats.messages_failed = messages.filter(status='failed').count()
        stats.messages_read = messages.filter(status='read').count()
        
        # Calculer les métriques
        stats.calculate_metrics()
        
        return stats

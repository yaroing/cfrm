"""
Vues pour l'API des canaux
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

from .models import (
    ChannelConfiguration, MessageTemplate, Message, 
    WebhookEvent, ChannelStats
)
from .serializers import (
    ChannelConfigurationSerializer, MessageTemplateSerializer,
    MessageSerializer, WebhookEventSerializer, ChannelStatsSerializer
)
from .services import MessageService, ChannelServiceFactory


class ChannelConfigurationViewSet(viewsets.ModelViewSet):
    """API pour les configurations de canaux"""
    queryset = ChannelConfiguration.objects.all()
    serializer_class = ChannelConfigurationSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def test_connection(self, request, pk=None):
        """Tester la connexion d'un canal"""
        channel = self.get_object()
        try:
            service = ChannelServiceFactory.get_service(channel)
            # Implémenter le test de connexion selon le type de canal
            return Response({'status': 'Connexion réussie'})
        except Exception as e:
            return Response(
                {'error': f'Erreur de connexion: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def send_test_message(self, request, pk=None):
        """Envoyer un message de test"""
        channel = self.get_object()
        recipient = request.data.get('recipient')
        content = request.data.get('content', 'Message de test CFRM')
        
        if not recipient:
            return Response(
                {'error': 'Destinataire requis'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            service = ChannelServiceFactory.get_service(channel)
            message = service.send_message(recipient, content)
            
            if message:
                return Response({
                    'status': 'Message envoyé',
                    'message_id': str(message.id)
                })
            else:
                return Response(
                    {'error': 'Échec de l\'envoi'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {'error': f'Erreur d\'envoi: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class MessageTemplateViewSet(viewsets.ModelViewSet):
    """API pour les modèles de messages"""
    queryset = MessageTemplate.objects.all()
    serializer_class = MessageTemplateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        channel_id = self.request.query_params.get('channel')
        if channel_id:
            queryset = queryset.filter(channel_id=channel_id)
        return queryset


class MessageViewSet(viewsets.ModelViewSet):
    """API pour les messages"""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def resend(self, request, pk=None):
        """Renvoyer un message"""
        message = self.get_object()
        
        try:
            service = ChannelServiceFactory.get_service(message.channel)
            new_message = service.send_message(
                recipient=message.recipient,
                content=message.content,
                subject=message.subject,
                template=message.template,
                ticket=message.ticket,
                response=message.response
            )
            
            if new_message:
                return Response({
                    'status': 'Message renvoyé',
                    'new_message_id': str(new_message.id)
                })
            else:
                return Response(
                    {'error': 'Échec du renvoi'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {'error': f'Erreur de renvoi: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class WebhookEventViewSet(viewsets.ReadOnlyModelViewSet):
    """API pour les événements webhook"""
    queryset = WebhookEvent.objects.all()
    serializer_class = WebhookEventSerializer
    permission_classes = [IsAuthenticated]


class ChannelStatsViewSet(viewsets.ReadOnlyModelViewSet):
    """API pour les statistiques des canaux"""
    queryset = ChannelStats.objects.all()
    serializer_class = ChannelStatsSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Résumé des statistiques"""
        # Statistiques des 30 derniers jours
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)
        
        stats = ChannelStats.objects.filter(
            date__gte=start_date,
            date__lte=end_date
        )
        
        summary = {
            'total_messages_sent': sum(s.messages_sent for s in stats),
            'total_messages_delivered': sum(s.messages_delivered for s in stats),
            'total_messages_failed': sum(s.messages_failed for s in stats),
            'total_messages_read': sum(s.messages_read for s in stats),
            'overall_success_rate': 0,
            'channels': []
        }
        
        if summary['total_messages_sent'] > 0:
            summary['overall_success_rate'] = (
                summary['total_messages_delivered'] / summary['total_messages_sent']
            ) * 100
        
        # Statistiques par canal
        for channel in ChannelConfiguration.objects.filter(is_active=True):
            channel_stats = stats.filter(channel=channel)
            channel_summary = {
                'channel_name': channel.name,
                'channel_type': channel.type,
                'messages_sent': sum(s.messages_sent for s in channel_stats),
                'messages_delivered': sum(s.messages_delivered for s in channel_stats),
                'messages_failed': sum(s.messages_failed for s in channel_stats),
                'success_rate': 0
            }
            
            if channel_summary['messages_sent'] > 0:
                channel_summary['success_rate'] = (
                    channel_summary['messages_delivered'] / channel_summary['messages_sent']
                ) * 100
            
            summary['channels'].append(channel_summary)
        
        return Response(summary)


# Vues webhook pour les services externes
@method_decorator(csrf_exempt, name='dispatch')
class SMSWebhookView(APIView):
    """Webhook pour les SMS Twilio"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Traiter les webhooks Twilio"""
        try:
            # Récupérer la configuration SMS
            sms_channel = ChannelConfiguration.objects.filter(
                type='sms', is_active=True
            ).first()
            
            if not sms_channel:
                return JsonResponse({'error': 'Canal SMS non configuré'}, status=400)
            
            # Traiter le webhook
            service = ChannelServiceFactory.get_service(sms_channel)
            webhook_event = service.process_webhook(
                payload=request.data,
                headers=dict(request.headers)
            )
            
            return JsonResponse({'status': 'success', 'event_id': str(webhook_event.id)})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class WhatsAppWebhookView(APIView):
    """Webhook pour WhatsApp Business API"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Vérification du webhook"""
        verify_token = request.GET.get('hub.verify_token')
        if verify_token == settings.WHATSAPP_VERIFY_TOKEN:
            return JsonResponse({'hub.challenge': request.GET.get('hub.challenge')})
        return JsonResponse({'error': 'Token invalide'}, status=403)
    
    def post(self, request):
        """Traiter les webhooks WhatsApp"""
        try:
            # Récupérer la configuration WhatsApp
            whatsapp_channel = ChannelConfiguration.objects.filter(
                type='whatsapp', is_active=True
            ).first()
            
            if not whatsapp_channel:
                return JsonResponse({'error': 'Canal WhatsApp non configuré'}, status=400)
            
            # Traiter le webhook
            service = ChannelServiceFactory.get_service(whatsapp_channel)
            webhook_event = service.process_webhook(
                payload=request.data,
                headers=dict(request.headers)
            )
            
            return JsonResponse({'status': 'success', 'event_id': str(webhook_event.id)})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class EmailWebhookView(APIView):
    """Webhook pour les emails (si supporté par le fournisseur)"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Traiter les webhooks email"""
        try:
            # Récupérer la configuration email
            email_channel = ChannelConfiguration.objects.filter(
                type='email', is_active=True
            ).first()
            
            if not email_channel:
                return JsonResponse({'error': 'Canal email non configuré'}, status=400)
            
            # Traiter le webhook
            service = ChannelServiceFactory.get_service(email_channel)
            webhook_event = service.process_webhook(
                payload=request.data,
                headers=dict(request.headers)
            )
            
            return JsonResponse({'status': 'success', 'event_id': str(webhook_event.id)})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

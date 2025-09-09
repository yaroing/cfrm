"""
Sérialiseurs pour l'API des canaux
"""
from rest_framework import serializers
from .models import (
    ChannelConfiguration, MessageTemplate, Message, 
    WebhookEvent, ChannelStats
)


class ChannelConfigurationSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = ChannelConfiguration
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class MessageTemplateSerializer(serializers.ModelSerializer):
    channel_name = serializers.CharField(source='channel.name', read_only=True)
    template_type_display = serializers.CharField(source='get_template_type_display', read_only=True)
    
    class Meta:
        model = MessageTemplate
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class MessageSerializer(serializers.ModelSerializer):
    channel_name = serializers.CharField(source='channel.name', read_only=True)
    channel_type = serializers.CharField(source='channel.type', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    ticket_id = serializers.CharField(source='ticket.id', read_only=True)
    response_id = serializers.CharField(source='response.id', read_only=True)
    
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = [
            'id', 'created_at', 'sent_at', 'delivered_at', 'read_at'
        ]


class WebhookEventSerializer(serializers.ModelSerializer):
    event_type_display = serializers.CharField(source='get_event_type_display', read_only=True)
    channel_name = serializers.CharField(source='channel.name', read_only=True)
    message_id = serializers.CharField(source='message.id', read_only=True)
    ticket_id = serializers.CharField(source='ticket.id', read_only=True)
    
    class Meta:
        model = WebhookEvent
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'processed_at']


class ChannelStatsSerializer(serializers.ModelSerializer):
    channel_name = serializers.CharField(source='channel.name', read_only=True)
    channel_type = serializers.CharField(source='channel.type', read_only=True)
    
    class Meta:
        model = ChannelStats
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

"""
URLs pour l'API des canaux
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'channels', views.ChannelConfigurationViewSet)
router.register(r'templates', views.MessageTemplateViewSet)
router.register(r'messages', views.MessageViewSet)
router.register(r'webhooks', views.WebhookEventViewSet)
router.register(r'stats', views.ChannelStatsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('webhooks/sms/', views.SMSWebhookView.as_view(), name='sms-webhook'),
    path('webhooks/whatsapp/', views.WhatsAppWebhookView.as_view(), name='whatsapp-webhook'),
    path('webhooks/email/', views.EmailWebhookView.as_view(), name='email-webhook'),
]

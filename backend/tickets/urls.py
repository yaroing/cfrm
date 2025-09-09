"""
URLs pour l'API des tickets
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import import_views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'priorities', views.PriorityViewSet)
router.register(r'statuses', views.StatusViewSet)
router.register(r'channels', views.ChannelViewSet)
router.register(r'tickets', views.TicketViewSet)
router.register(r'responses', views.ResponseViewSet)
router.register(r'logs', views.TicketLogViewSet)
router.register(r'feedback', views.FeedbackViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('tickets/import/', import_views.import_tickets, name='import-tickets'),
]

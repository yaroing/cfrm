"""
Vues pour l'API des tickets
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg, F, ExpressionWrapper, DurationField
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.contrib.auth import get_user_model

from .models import (
    Category, Priority, Status, Channel, Ticket, 
    Response as TicketResponse, TicketLog, Feedback
)
from .serializers import (
    CategorySerializer, PrioritySerializer, StatusSerializer, 
    ChannelSerializer, TicketSerializer, TicketCreateSerializer,
    TicketUpdateSerializer, ResponseSerializer, TicketLogSerializer,
    FeedbackSerializer
)
from .filters import TicketFilter
from channels.services import MessageService


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API pour les catégories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class PriorityViewSet(viewsets.ReadOnlyModelViewSet):
    """API pour les priorités"""
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer
    permission_classes = [AllowAny]


class StatusViewSet(viewsets.ReadOnlyModelViewSet):
    """API pour les statuts"""
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [AllowAny]


class ChannelViewSet(viewsets.ReadOnlyModelViewSet):
    """API pour les canaux"""
    queryset = Channel.objects.filter(is_active=True)
    serializer_class = ChannelSerializer
    permission_classes = [AllowAny]


class TicketViewSet(viewsets.ModelViewSet):
    """API pour les tickets"""
    queryset = Ticket.objects.all()
    permission_classes = [AllowAny]  # Permettre l'accès public pour créer et voir les tickets
    filterset_class = TicketFilter
    search_fields = ['title', 'content', 'submitter_name', 'submitter_phone', 'submitter_email']
    ordering_fields = ['created_at', 'updated_at', 'priority__level', 'status__name']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return TicketCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TicketUpdateSerializer
        return TicketSerializer

    def list(self, request, *args, **kwargs):
        """Liste des tickets avec gestion sûre de la pagination (jamais 404 sur page vide)."""
        queryset = self.filter_queryset(self.get_queryset())

        try:
            page = self.paginate_queryset(queryset)
        except Exception:
            # En cas d'erreur de pagination (page invalide, hors plage), renvoyer une page vide
            return self.get_paginated_response([])

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        """Filtrer les tickets selon les permissions de l'utilisateur"""
        queryset = super().get_queryset()
        
        # Si l'utilisateur n'est pas authentifié, retourner tous les tickets
        if not self.request.user.is_authenticated:
            return queryset
        
        # Si l'utilisateur n'est pas superuser, filtrer selon les rôles
        if not self.request.user.is_superuser:
            # Logique de filtrage basée sur les rôles
            # À implémenter selon les besoins spécifiques
            pass
        
        return queryset

    def perform_create(self, serializer):
        """Créer un ticket, définir le statut par défaut si absent et envoyer un accusé de réception."""
        ticket = serializer.save()

        # Définir un statut par défaut 'Ouvert' si non renseigné par le sérializer
        if not ticket.status:
            ticket.status = Status.objects.filter(name='Ouvert').first()
            ticket.save(update_fields=['status'])

        # Enregistrer l'auteur si authentifié
        if self.request and self.request.user and self.request.user.is_authenticated:
            if ticket.created_by_id is None:
                ticket.created_by = self.request.user
                ticket.save(update_fields=['created_by'])

        # Envoyer un accusé de réception (best-effort)
        try:
            MessageService.send_ticket_confirmation(ticket)
        except Exception:
            # Ne pas bloquer la création du ticket si l'envoi échoue
            pass

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """Assigner un ticket à un utilisateur"""
        ticket = self.get_object()
        assigned_to_id = request.data.get('assigned_to')
        
        if assigned_to_id:
            try:
                user = get_user_model().objects.get(id=assigned_to_id)
                ticket.assigned_to = user
                ticket.save()
                
                TicketLog.objects.create(
                    ticket=ticket,
                    action='assigned',
                    user=request.user,
                    description=f"Ticket assigné à {user.get_full_name()}",
                    new_value=str(user)
                )
                
                return Response({'status': 'Ticket assigné'})
            except User.DoesNotExist:
                return Response({'error': 'Utilisateur non trouvé'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'error': 'ID utilisateur requis'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        """Fermer un ticket"""
        ticket = self.get_object()
        ticket.status = Status.objects.filter(name='Fermé').first()
        ticket.closed_at = timezone.now()
        ticket.save()
        
        TicketLog.objects.create(
            ticket=ticket,
            action='closed',
            user=request.user,
            description="Ticket fermé"
        )
        
        return Response({'status': 'Ticket fermé'})

    @action(detail=True, methods=['post'])
    def reopen(self, request, pk=None):
        """Rouvrir un ticket"""
        ticket = self.get_object()
        ticket.status = Status.objects.filter(name='Ouvert').first()
        ticket.closed_at = None
        ticket.save()
        
        TicketLog.objects.create(
            ticket=ticket,
            action='reopened',
            user=request.user,
            description="Ticket rouvert"
        )
        
        return Response({'status': 'Ticket rouvert'})

    @action(detail=True, methods=['post'])
    def escalate(self, request, pk=None):
        """Escalader un ticket"""
        ticket = self.get_object()
        escalated_to = request.data.get('escalated_to')
        
        if escalated_to:
            ticket.escalated_at = timezone.now()
            ticket.escalated_to = escalated_to
            ticket.save()
            
            TicketLog.objects.create(
                ticket=ticket,
                action='escalated',
                user=request.user,
                description=f"Ticket escaladé vers {escalated_to}",
                new_value=escalated_to
            )
            
            return Response({'status': 'Ticket escaladé'})
        
        return Response({'error': 'Email de destination requis'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Statistiques d'un ticket"""
        ticket = self.get_object()
        
        stats = {
            'days_since_creation': ticket.days_since_creation,
            'is_overdue': ticket.is_overdue,
            'responses_count': ticket.responses.count(),
            'logs_count': ticket.logs.count(),
            'has_feedback': hasattr(ticket, 'feedback'),
        }
        
        feedback = getattr(ticket, 'feedback', None)
        if feedback is not None:
            stats['feedback'] = FeedbackSerializer(feedback).data
        
        return Response(stats)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def dashboard_stats(self, request):
        """Statistiques pour le tableau de bord"""
        from django.db.models import Count, Q
        from django.utils import timezone
        from datetime import timedelta
        
        # Statistiques par statut
        status_stats = list(
            Ticket.objects.values('status__name')
            .annotate(count=Count('id'))
            .order_by('status__name')
        )
        
        # Statistiques par catégorie
        category_stats = list(
            Ticket.objects.values('category__name')
            .annotate(count=Count('id'))
            .order_by('category__name')
        )
        
        # Statistiques par canal
        channel_stats = list(
            Ticket.objects.values('channel__name')
            .annotate(count=Count('id'))
            .order_by('channel__name')
        )
        
        # Tickets en retard (SLA dépassé)
        overdue_count = Ticket.objects.filter(
            sla_deadline__lt=timezone.now(),
            status__is_final=False
        ).count()
        
        # Tickets de cette semaine
        week_start = timezone.now() - timedelta(days=7)
        weekly_tickets = Ticket.objects.filter(
            created_at__gte=week_start
        ).count()
        
        # Temps de réponse moyen (simplifié)
        avg_response_time = None
        
        return Response({
            'status_stats': status_stats,
            'category_stats': category_stats,
            'channel_stats': channel_stats,
            'overdue_count': overdue_count,
            'weekly_tickets': weekly_tickets,
            'avg_response_time': avg_response_time
        })


class ResponseViewSet(viewsets.ModelViewSet):
    """API pour les réponses"""
    queryset = TicketResponse.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [AllowAny]  # Permettre l'accès public pour les réponses

    def get_queryset(self):
        """Filtrer les réponses par ticket si le paramètre ticket est fourni"""
        queryset = super().get_queryset()
        ticket_id = self.request.query_params.get('ticket', None)
        if ticket_id:
            queryset = queryset.filter(ticket_id=ticket_id)
        return queryset

    def perform_create(self, serializer):
        # Ne pas définir l'auteur si l'utilisateur n'est pas authentifié
        if self.request.user.is_authenticated:
            serializer.save(author=self.request.user)
        else:
            serializer.save()


class TicketLogViewSet(viewsets.ReadOnlyModelViewSet):
    """API pour les logs de tickets"""
    queryset = TicketLog.objects.all()
    serializer_class = TicketLogSerializer
    permission_classes = [AllowAny]  # Permettre l'accès public pour les logs
    filterset_fields = ['ticket', 'action', 'user']
    ordering = ['-created_at']


class FeedbackViewSet(viewsets.ModelViewSet):
    """API pour les feedbacks de satisfaction"""
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [AllowAny]  # Permettre aux utilisateurs externes de donner leur avis

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Statistiques des feedbacks"""
        stats = Feedback.objects.aggregate(
            avg_satisfaction=Avg('satisfaction_rating'),
            avg_response_time=Avg('response_time_rating'),
            avg_quality=Avg('quality_rating'),
            total_count=Count('id'),
            recommend_count=Count('id', filter=Q(would_recommend=True))
        )
        
        return Response(stats)

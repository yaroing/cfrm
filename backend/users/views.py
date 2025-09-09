"""
Vues pour l'API des utilisateurs
"""
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from .models import Organization, Role, User, UserActivity, UserPreference
from .serializers import (
    OrganizationSerializer, RoleSerializer, UserSerializer,
    UserCreateSerializer, UserUpdateSerializer, PasswordChangeSerializer,
    LoginSerializer, UserStatsSerializer, UserPreferenceSerializer
)


class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    """API pour les organisations"""
    queryset = Organization.objects.filter(is_active=True)
    serializer_class = OrganizationSerializer
    permission_classes = [AllowAny]


class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    """API pour les rôles"""
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [AllowAny]  # Permettre l'accès public pour les rôles


class UserViewSet(viewsets.ModelViewSet):
    """API pour les utilisateurs"""
    queryset = User.objects.all()
    permission_classes = [AllowAny]  # Permettre l'accès public pour l'assignation des tickets
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer
    
    def get_queryset(self):
        """Filtrer les utilisateurs selon les permissions"""
        queryset = super().get_queryset()
        
        # Si l'utilisateur n'est pas superuser, ne pas afficher les superusers
        if not self.request.user.is_superuser:
            queryset = queryset.filter(is_superuser=False)
        
        return queryset
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """Connexion utilisateur"""
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            
            # Enregistrer l'activité
            UserActivity.objects.create(
                user=user,
                action='login',
                description=f"Connexion depuis {request.META.get('REMOTE_ADDR')}",
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            # Mettre à jour la dernière activité
            user.update_last_activity()
            
            # Générer des tokens JWT pour le frontend
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data,
                'message': 'Connexion réussie'
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """Déconnexion utilisateur"""
        # Enregistrer l'activité
        UserActivity.objects.create(
            user=request.user,
            action='logout',
            description=f"Déconnexion depuis {request.META.get('REMOTE_ADDR')}",
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        logout(request)
        return Response({'message': 'Déconnexion réussie'})
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Informations de l'utilisateur connecté"""
        return Response(UserSerializer(request.user).data)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Changement de mot de passe"""
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            
            # Enregistrer l'activité
            UserActivity.objects.create(
                user=request.user,
                action='password_change',
                description="Changement de mot de passe",
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            return Response({'message': 'Mot de passe modifié avec succès'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activer un utilisateur"""
        user = self.get_object()
        user.is_active = True
        user.save()
        
        UserActivity.objects.create(
            user=request.user,
            action='user_activate',
            description=f"Utilisateur {user.username} activé",
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return Response({'message': 'Utilisateur activé'})
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Désactiver un utilisateur"""
        user = self.get_object()
        user.is_active = False
        user.save()
        
        UserActivity.objects.create(
            user=request.user,
            action='user_deactivate',
            description=f"Utilisateur {user.username} désactivé",
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return Response({'message': 'Utilisateur désactivé'})
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Statistiques des utilisateurs"""
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        verified_users = User.objects.filter(is_verified=True).count()
        
        # Utilisateurs par organisation
        users_by_organization = User.objects.values('organization__name').annotate(
            count=Count('id')
        ).order_by('organization__name')
        
        # Utilisateurs par rôle
        users_by_role = User.objects.values('role__name').annotate(
            count=Count('id')
        ).order_by('role__name')
        
        # Connexions récentes (dernières 24h)
        recent_logins = User.objects.filter(
            last_login__gte=timezone.now() - timedelta(days=1)
        ).count()
        
        stats = {
            'total_users': total_users,
            'active_users': active_users,
            'verified_users': verified_users,
            'users_by_organization': list(users_by_organization),
            'users_by_role': list(users_by_role),
            'recent_logins': recent_logins,
        }
        
        return Response(stats)


class AuthLoginView(APIView):
    """Endpoint de connexion sans authentification préalable (AllowAny)"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)

            # Enregistrer l'activité
            UserActivity.objects.create(
                user=user,
                action='login',
                description=f"Connexion depuis {request.META.get('REMOTE_ADDR')}",
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )

            # Mettre à jour la dernière activité
            user.update_last_activity()

            # Générer des tokens JWT pour le frontend
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data,
                'message': 'Connexion réussie'
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserPreferenceViewSet(viewsets.ModelViewSet):
    """API pour les préférences utilisateur"""
    queryset = UserPreference.objects.all()
    serializer_class = UserPreferenceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserPreference.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_preferences(self, request):
        """Préférences de l'utilisateur connecté"""
        preferences, created = UserPreference.objects.get_or_create(user=request.user)
        return Response(UserPreferenceSerializer(preferences).data)
    
    @action(detail=False, methods=['post'])
    def update_preferences(self, request):
        """Mise à jour des préférences"""
        preferences, created = UserPreference.objects.get_or_create(user=request.user)
        serializer = UserPreferenceSerializer(preferences, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
Vues pour l'importation de tickets
"""
import csv
import io
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.utils import timezone
from .models import Ticket, Category, Priority, Channel, Status


@api_view(['POST'])
@permission_classes([AllowAny])
def import_tickets(request):
    """
    Importe des tickets depuis un fichier CSV
    """
    if 'file' not in request.FILES:
        return Response(
            {'message': 'Aucun fichier fourni'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    file = request.FILES['file']
    
    # Vérifier que c'est un fichier CSV
    if not file.name.endswith('.csv'):
        return Response(
            {'message': 'Le fichier doit être au format CSV'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Lire le contenu du fichier
        content = file.read().decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(content))
        
        imported_count = 0
        errors = []
        
        # Obtenir les objets de référence
        categories = {cat.name: cat for cat in Category.objects.all()}
        priorities = {pri.name: pri for pri in Priority.objects.all()}
        channels = {ch.name: ch for ch in Channel.objects.all()}
        statuses = {st.name: st for st in Status.objects.all()}
        
        # Canal par défaut
        default_channel = channels.get('Portail Web')
        if not default_channel:
            default_channel = Channel.objects.first()
        
        # Statut par défaut
        default_status = statuses.get('Ouvert')
        if not default_status:
            default_status = Status.objects.first()
        
        # Priorité par défaut
        default_priority = priorities.get('Moyenne')
        if not default_priority:
            default_priority = Priority.objects.first()
        
        with transaction.atomic():
            for row_num, row in enumerate(csv_reader, start=2):  # Commencer à 2 car la ligne 1 est l'en-tête
                try:
                    # Validation des champs requis
                    if not row.get('title') or not row.get('content'):
                        errors.append(f"Ligne {row_num}: Le titre et le contenu sont requis")
                        continue
                    
                    # Récupérer les objets de référence
                    category = categories.get(row.get('category', ''))
                    if not category:
                        errors.append(f"Ligne {row_num}: Catégorie '{row.get('category')}' non trouvée")
                        continue
                    
                    priority = priorities.get(row.get('priority', ''))
                    if not priority:
                        priority = default_priority
                    
                    channel = channels.get(row.get('channel', ''))
                    if not channel:
                        channel = default_channel
                    
                    # Créer le ticket
                    ticket = Ticket.objects.create(
                        title=row['title'],
                        content=row['content'],
                        category=category,
                        priority=priority,
                        channel=channel,
                        status=default_status,
                        submitter_name=row.get('submitter_name', ''),
                        submitter_phone=row.get('submitter_phone', ''),
                        submitter_email=row.get('submitter_email', ''),
                        submitter_location=row.get('submitter_location', ''),
                        is_anonymous=row.get('is_anonymous', '').lower() in ['true', '1', 'yes', 'oui'],
                    )
                    
                    imported_count += 1
                    
                except Exception as e:
                    errors.append(f"Ligne {row_num}: Erreur lors de la création du ticket - {str(e)}")
                    continue
        
        return Response({
            'message': f'Importation terminée. {imported_count} tickets importés.',
            'imported_count': imported_count,
            'errors': errors
        })
        
    except Exception as e:
        return Response(
            {'message': f'Erreur lors de la lecture du fichier: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

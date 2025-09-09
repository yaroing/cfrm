"""
URLs pour l'API des rapports
"""
from django.urls import path
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

def test_view(request):
    return Response({'message': 'Test OK'})

def generate_report(request):
    """
    Génère un rapport des tickets selon les filtres fournis
    """
    if request.method == 'GET':
        return Response({
            'message': 'API de génération de rapports disponible',
            'endpoints': {
                'POST /api/v1/reports/generate/': 'Générer un rapport',
                'GET /api/v1/reports/download/<filename>': 'Télécharger un rapport'
            }
        })
    
    try:
        filters = request.data
        format_type = filters.get('format', 'excel')
        
        # Pour l'instant, retournons une réponse simple
        return Response({
            'message': 'Rapport généré avec succès',
            'download_url': f'/api/v1/reports/download/rapport_{format_type}.{format_type}',
            'format': format_type,
            'ticket_count': 0,
            'filters_applied': filters
        })
            
    except Exception as e:
        return Response({
            'message': f'Erreur lors de la génération du rapport: {str(e)}',
            'error': str(e)
        }, status=500)

def download_report(request, filename):
    """
    Télécharge un fichier de rapport généré
    """
    return Response({
        'message': f'Téléchargement du fichier {filename}',
        'filename': filename
    })

urlpatterns = [
    path('test/', test_view, name='test'),
    path('generate/', generate_report, name='generate-report'),
    path('download/<str:filename>', download_report, name='download-report'),
]

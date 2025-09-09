"""
Commande Django pour initialiser les données de base
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Organization, Role
from tickets.models import Category, Priority, Status
from channels.models import ChannelConfiguration, MessageTemplate
from analytics.models import Metric, Dashboard

User = get_user_model()


class Command(BaseCommand):
    help = 'Initialise les données de base de la plateforme CFRM'

    def handle(self, *args, **options):
        self.stdout.write('Initialisation des données de base...')

        # Créer l'organisation par défaut
        org, created = Organization.objects.get_or_create(
            code='CFRM',
            defaults={
                'name': 'CFRM Platform',
                'description': 'Plateforme de feedback communautaire',
                'contact_email': 'admin@cfrm.org',
                'is_active': True
            }
        )
        if created:
            self.stdout.write(f'✓ Organisation créée: {org.name}')
        else:
            self.stdout.write(f'✓ Organisation existante: {org.name}')

        # Créer les rôles
        roles_data = [
            {
                'name': 'Admin',
                'description': 'Administrateur système',
                'permissions': ['all'],
                'is_psea_authorized': True,
                'can_escalate': True,
                'can_assign': True,
                'can_close': True,
                'can_view_analytics': True,
            },
            {
                'name': 'Manager',
                'description': 'Gestionnaire',
                'permissions': ['view_tickets', 'edit_tickets', 'assign_tickets', 'close_tickets', 'view_analytics'],
                'is_psea_authorized': True,
                'can_escalate': True,
                'can_assign': True,
                'can_close': True,
                'can_view_analytics': True,
            },
            {
                'name': 'Agent',
                'description': 'Agent de traitement',
                'permissions': ['view_tickets', 'edit_tickets', 'create_responses'],
                'is_psea_authorized': False,
                'can_escalate': False,
                'can_assign': False,
                'can_close': False,
                'can_view_analytics': False,
            },
            {
                'name': 'PSEA_Focal_Point',
                'description': 'Point focal PSEA',
                'permissions': ['view_tickets', 'edit_tickets', 'psea_access', 'escalate_tickets'],
                'is_psea_authorized': True,
                'can_escalate': True,
                'can_assign': False,
                'can_close': False,
                'can_view_analytics': False,
            },
        ]

        for role_data in roles_data:
            role, created = Role.objects.get_or_create(
                name=role_data['name'],
                defaults=role_data
            )
            if created:
                self.stdout.write(f'✓ Rôle créé: {role.name}')
            else:
                self.stdout.write(f'✓ Rôle existant: {role.name}')

        # Créer les catégories
        categories_data = [
            {
                'name': 'Information',
                'description': 'Demande d\'information générale',
                'is_sensitive': False,
                'requires_escalation': False,
                'escalation_contact': '',
            },
            {
                'name': 'Complaint',
                'description': 'Plainte générale',
                'is_sensitive': False,
                'requires_escalation': True,
                'escalation_contact': 'complaints@cfrm.org',
            },
            {
                'name': 'PSEA',
                'description': 'Protection contre l\'exploitation et les abus sexuels',
                'is_sensitive': True,
                'requires_escalation': True,
                'escalation_contact': 'psea@cfrm.org',
            },
            {
                'name': 'Request',
                'description': 'Demande de service',
                'is_sensitive': False,
                'requires_escalation': False,
                'escalation_contact': '',
            },
            {
                'name': 'Feedback',
                'description': 'Retour d\'expérience',
                'is_sensitive': False,
                'requires_escalation': False,
                'escalation_contact': '',
            },
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'✓ Catégorie créée: {category.name}')
            else:
                self.stdout.write(f'✓ Catégorie existante: {category.name}')

        # Créer les priorités
        priorities_data = [
            {'name': 'Critique', 'level': 5, 'color': '#DC2626', 'sla_hours': 2},
            {'name': 'Élevée', 'level': 4, 'color': '#EA580C', 'sla_hours': 4},
            {'name': 'Moyenne', 'level': 3, 'color': '#D97706', 'sla_hours': 24},
            {'name': 'Faible', 'level': 2, 'color': '#16A34A', 'sla_hours': 72},
            {'name': 'Information', 'level': 1, 'color': '#2563EB', 'sla_hours': 168},
        ]

        for prio_data in priorities_data:
            priority, created = Priority.objects.get_or_create(
                name=prio_data['name'],
                defaults=prio_data
            )
            if created:
                self.stdout.write(f'✓ Priorité créée: {priority.name}')
            else:
                self.stdout.write(f'✓ Priorité existante: {priority.name}')

        # Créer les statuts
        statuses_data = [
            {'name': 'Ouvert', 'description': 'Ticket nouvellement créé', 'is_final': False, 'color': '#3B82F6'},
            {'name': 'En cours', 'description': 'Ticket en cours de traitement', 'is_final': False, 'color': '#F59E0B'},
            {'name': 'En attente', 'description': 'Ticket en attente de réponse', 'is_final': False, 'color': '#8B5CF6'},
            {'name': 'Escaladé', 'description': 'Ticket escaladé vers un niveau supérieur', 'is_final': False, 'color': '#EF4444'},
            {'name': 'Fermé', 'description': 'Ticket fermé', 'is_final': True, 'color': '#10B981'},
            {'name': 'Annulé', 'description': 'Ticket annulé', 'is_final': True, 'color': '#6B7280'},
        ]

        for status_data in statuses_data:
            status, created = Status.objects.get_or_create(
                name=status_data['name'],
                defaults=status_data
            )
            if created:
                self.stdout.write(f'✓ Statut créé: {status.name}')
            else:
                self.stdout.write(f'✓ Statut existant: {status.name}')

        # Créer les canaux
        channels_data = [
            {
                'name': 'SMS Twilio',
                'type': 'sms',
                'is_active': True,
                'configuration': {'provider': 'twilio', 'phone_number': '+1234567890'},
            },
            {
                'name': 'WhatsApp Business',
                'type': 'whatsapp',
                'is_active': True,
                'configuration': {'provider': 'whatsapp', 'phone_number_id': '123456789'},
            },
            {
                'name': 'Email SMTP',
                'type': 'email',
                'is_active': True,
                'configuration': {'provider': 'smtp', 'host': 'smtp.gmail.com', 'port': 587},
            },
            {
                'name': 'Portail Web',
                'type': 'web',
                'is_active': True,
                'configuration': {'provider': 'web', 'url': 'https://cfrm.org'},
            },
            {
                'name': 'Téléphone',
                'type': 'phone',
                'is_active': True,
                'configuration': {'provider': 'phone', 'number': '+1234567890'},
            },
        ]

        for channel_data in channels_data:
            channel, created = ChannelConfiguration.objects.get_or_create(
                name=channel_data['name'],
                defaults=channel_data
            )
            if created:
                self.stdout.write(f'✓ Canal créé: {channel.name}')
            else:
                self.stdout.write(f'✓ Canal existant: {channel.name}')

        # Créer des modèles de messages par défaut (idempotent)
        sms = ChannelConfiguration.objects.filter(type='sms').first()
        wa = ChannelConfiguration.objects.filter(type='whatsapp').first()
        email = ChannelConfiguration.objects.filter(type='email').first()
        templates = [
            {
                'name': 'Confirmation SMS',
                'channel': sms,
                'template_type': 'confirmation',
                'subject': '',
                'content': 'Merci pour votre message. Votre ticket #{ticket_id} a été reçu et sera traité dans les plus brefs délais.',
                'language': 'fr',
                'variables': ['ticket_id', 'title', 'category'],
                'is_active': True,
            },
            {
                'name': 'Confirmation WhatsApp',
                'channel': wa,
                'template_type': 'confirmation',
                'subject': '',
                'content': 'Merci pour votre message. Votre ticket #{ticket_id} a été reçu et sera traité dans les plus brefs délais.',
                'language': 'fr',
                'variables': ['ticket_id', 'title', 'category'],
                'is_active': True,
            },
            {
                'name': 'Confirmation Email',
                'channel': email,
                'template_type': 'confirmation',
                'subject': 'Confirmation de réception - Ticket #{ticket_id}',
                'content': "Bonjour,\n\nNous avons bien reçu votre message concernant : {title}\n\nVotre ticket #{ticket_id} a été enregistré dans la catégorie \"{category}\" avec la priorité \"{priority}\".\n\nNous vous répondrons dans les plus brefs délais.\n\nCordialement,\nL'équipe CFRM",
                'language': 'fr',
                'variables': ['ticket_id', 'title', 'category', 'priority'],
                'is_active': True,
            },
            {
                'name': 'Réponse SMS',
                'channel': sms,
                'template_type': 'response',
                'subject': '',
                'content': 'Réponse à votre ticket #{ticket_id} : {response_content}',
                'language': 'fr',
                'variables': ['ticket_id', 'response_content', 'responder'],
                'is_active': True,
            },
            {
                'name': 'Réponse WhatsApp',
                'channel': wa,
                'template_type': 'response',
                'subject': '',
                'content': 'Réponse à votre ticket #{ticket_id} :\n\n{response_content}\n\nRépondant : {responder}',
                'language': 'fr',
                'variables': ['ticket_id', 'response_content', 'responder'],
                'is_active': True,
            },
            {
                'name': 'Réponse Email',
                'channel': email,
                'template_type': 'response',
                'subject': 'Réponse à votre ticket #{ticket_id}',
                'content': "Bonjour,\n\nVoici la réponse à votre ticket #{ticket_id} :\n\n{response_content}\n\nRépondant : {responder}\n\nCordialement,\nL'équipe CFRM",
                'language': 'fr',
                'variables': ['ticket_id', 'response_content', 'responder'],
                'is_active': True,
            },
            {
                'name': 'Escalade PSEA',
                'channel': email,
                'template_type': 'escalation',
                'subject': 'URGENT - Escalade PSEA - Ticket #{ticket_id}',
                'content': 'URGENT : Ticket PSEA escaladé\n\nTicket #{ticket_id}\nTitre : {title}\nContenu : {content}\n\nAction requise immédiatement.',
                'language': 'fr',
                'variables': ['ticket_id', 'title', 'content'],
                'is_active': True,
            },
        ]

        for t in templates:
            if t['channel'] is None:
                continue
            obj, created = MessageTemplate.objects.get_or_create(
                name=t['name'], channel=t['channel'], template_type=t['template_type'], language=t['language'],
                defaults={k: v for k, v in t.items() if k not in ['name', 'channel', 'template_type', 'language']}
            )
            self.stdout.write(f"✓ Modèle {'créé' if created else 'existant'}: {obj.name} ({obj.template_type})")

        # Créer des métriques par défaut
        metrics = [
            {'name': 'Tickets créés', 'description': 'Nombre de tickets créés par jour', 'metric_type': 'counter', 'query': {'model': 'tickets.Ticket', 'field': 'created_at'}, 'unit': 'tickets', 'target_value': 100, 'warning_threshold': 150, 'critical_threshold': 200, 'is_active': True},
            {'name': 'Tickets fermés', 'description': 'Nombre de tickets fermés par jour', 'metric_type': 'counter', 'query': {'model': 'tickets.Ticket', 'field': 'closed_at'}, 'unit': 'tickets', 'target_value': 100, 'warning_threshold': 80, 'critical_threshold': 50, 'is_active': True},
            {'name': 'Temps de réponse moyen', 'description': 'Temps de réponse moyen en heures', 'metric_type': 'gauge', 'query': {'model': 'tickets.Ticket', 'calculation': 'avg_response_time'}, 'unit': 'heures', 'target_value': 24, 'warning_threshold': 48, 'critical_threshold': 72, 'is_active': True},
            {'name': 'Taux de satisfaction', 'description': 'Taux de satisfaction moyen', 'metric_type': 'gauge', 'query': {'model': 'tickets.Feedback', 'field': 'satisfaction_rating'}, 'unit': '%', 'target_value': 4.0, 'warning_threshold': 3.0, 'critical_threshold': 2.0, 'is_active': True},
            {'name': 'Tickets en retard', 'description': 'Nombre de tickets en retard de SLA', 'metric_type': 'counter', 'query': {'model': 'tickets.Ticket', 'filter': 'is_overdue'}, 'unit': 'tickets', 'target_value': 0, 'warning_threshold': 5, 'critical_threshold': 10, 'is_active': True},
        ]
        for m in metrics:
            obj, created = Metric.objects.get_or_create(name=m['name'], defaults=m)
            self.stdout.write(f"✓ Métrique {'créée' if created else 'existante'}: {obj.name}")

        # Créer un tableau de bord par défaut
        admin_user = User.objects.filter(username='admin').first()
        if admin_user:
            dash_defaults = {
                'description': 'Tableau de bord principal de la plateforme CFRM',
                'layout': {'columns': 3, 'rows': 4},
                'widgets': [
                    {'type': 'metric', 'title': 'Tickets ouverts', 'position': {'x': 0, 'y': 0, 'w': 1, 'h': 1}},
                    {'type': 'metric', 'title': 'Tickets fermés', 'position': {'x': 1, 'y': 0, 'w': 1, 'h': 1}},
                    {'type': 'metric', 'title': 'Temps de réponse', 'position': {'x': 2, 'y': 0, 'w': 1, 'h': 1}},
                    {'type': 'chart', 'title': 'Tickets par statut', 'position': {'x': 0, 'y': 1, 'w': 2, 'h': 2}},
                    {'type': 'chart', 'title': 'Tickets par canal', 'position': {'x': 2, 'y': 1, 'w': 1, 'h': 2}},
                ],
                'filters': {'date_range': 'last_30_days'},
                'is_public': True,
                'is_default': True,
                'created_by': admin_user,
            }
            dash, created = Dashboard.objects.get_or_create(name='Tableau de bord principal', defaults=dash_defaults)
            self.stdout.write(f"✓ Tableau de bord {'créé' if created else 'existant'}: {dash.name}")

        # Créer l'utilisateur admin
        admin_role = Role.objects.get(name='Admin')
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@cfrm.org',
                password='admin123',
                first_name='Admin',
                last_name='CFRM',
                organization=org,
                role=admin_role
            )
            self.stdout.write('✓ Superutilisateur créé: admin/admin123')
        else:
            self.stdout.write('✓ Superutilisateur existe déjà')

        self.stdout.write(
            self.style.SUCCESS('✓ Initialisation des données terminée avec succès!')
        )

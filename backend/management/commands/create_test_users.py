"""
Commande Django pour créer des utilisateurs de test avec les rôles appropriés
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Role, Organization
from django.db import transaction

User = get_user_model()


class Command(BaseCommand):
    help = 'Crée des utilisateurs de test avec les rôles Admin, Agent, Manager, PSEA_Focal_Point, Viewer'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Supprime les utilisateurs existants avant de créer les nouveaux',
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write('Suppression des utilisateurs de test existants...')
            User.objects.filter(username__startswith='test_').delete()

        # Créer une organisation de test si elle n'existe pas
        org, created = Organization.objects.get_or_create(
            name='Organisation de Test',
            defaults={
                'code': 'TEST',
                'description': 'Organisation pour les tests',
                'contact_email': 'test@example.com',
                'is_active': True
            }
        )
        if created:
            self.stdout.write(f'Organisation créée: {org.name}')
        else:
            self.stdout.write(f'Organisation existante: {org.name}')

        # Récupérer les rôles
        roles = {
            'Admin': Role.objects.get(name='Admin'),
            'Agent': Role.objects.get(name='Agent'),
            'Manager': Role.objects.get(name='Manager'),
            'PSEA_Focal_Point': Role.objects.get(name='PSEA_Focal_Point'),
            'Viewer': Role.objects.get(name='Viewer'),
        }

        # Définir les utilisateurs de test
        test_users = [
            {
                'username': 'test_admin',
                'email': 'admin@test.com',
                'first_name': 'Admin',
                'last_name': 'Test',
                'role': roles['Admin'],
                'password': 'admin123',
                'is_staff': True,
                'is_superuser': True,
            },
            {
                'username': 'test_manager',
                'email': 'manager@test.com',
                'first_name': 'Manager',
                'last_name': 'Test',
                'role': roles['Manager'],
                'password': 'manager123',
                'is_staff': True,
                'is_superuser': False,
            },
            {
                'username': 'test_agent',
                'email': 'agent@test.com',
                'first_name': 'Agent',
                'last_name': 'Test',
                'role': roles['Agent'],
                'password': 'agent123',
                'is_staff': False,
                'is_superuser': False,
            },
            {
                'username': 'test_psea',
                'email': 'psea@test.com',
                'first_name': 'PSEA',
                'last_name': 'Focal Point',
                'role': roles['PSEA_Focal_Point'],
                'password': 'psea123',
                'is_staff': True,
                'is_superuser': False,
            },
            {
                'username': 'test_viewer',
                'email': 'viewer@test.com',
                'first_name': 'Viewer',
                'last_name': 'Test',
                'role': roles['Viewer'],
                'password': 'viewer123',
                'is_staff': False,
                'is_superuser': False,
            },
        ]

        with transaction.atomic():
            for user_data in test_users:
                username = user_data['username']
                
                # Vérifier si l'utilisateur existe déjà
                if User.objects.filter(username=username).exists():
                    self.stdout.write(f'Utilisateur {username} existe déjà, mise à jour...')
                    user = User.objects.get(username=username)
                    for key, value in user_data.items():
                        if key != 'password':
                            setattr(user, key, value)
                    user.set_password(user_data['password'])
                    user.save()
                else:
                    self.stdout.write(f'Création de l\'utilisateur {username}...')
                    user = User.objects.create_user(
                        username=username,
                        email=user_data['email'],
                        first_name=user_data['first_name'],
                        last_name=user_data['last_name'],
                        password=user_data['password'],
                        is_staff=user_data['is_staff'],
                        is_superuser=user_data['is_superuser'],
                        organization=org,
                        role=user_data['role'],
                        is_active=True,
                        is_verified=True,
                    )

                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Utilisateur {username} créé/mis à jour - Rôle: {user_data["role"].name}'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS('\n🎉 Tous les utilisateurs de test ont été créés avec succès!')
        )
        
        self.stdout.write('\n📋 Informations de connexion:')
        self.stdout.write('=' * 50)
        for user_data in test_users:
            self.stdout.write(f'👤 {user_data["first_name"]} {user_data["last_name"]}')
            self.stdout.write(f'   Username: {user_data["username"]}')
            self.stdout.write(f'   Password: {user_data["password"]}')
            self.stdout.write(f'   Email: {user_data["email"]}')
            self.stdout.write(f'   Rôle: {user_data["role"].name}')
            self.stdout.write('   Permissions:')
            for permission in user_data["role"].permissions:
                self.stdout.write(f'     - {permission}')
            self.stdout.write('')



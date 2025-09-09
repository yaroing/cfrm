from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model

from tickets.models import Category, Priority, Status, Channel, Ticket


class Command(BaseCommand):
    help = "Seed basic Categories, Priorities, Statuses, Channels and a few demo Tickets"

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("Seeding tickets basics..."))

        # Categories
        cats = [
            ("Information", dict(description="Demande d'information générale", is_sensitive=False)),
            ("Complaint", dict(description="Plainte générale", is_sensitive=False)),
            ("PSEA", dict(description="Protection contre l'exploitation et les abus sexuels", is_sensitive=True)),
        ]
        for name, extra in cats:
            Category.objects.get_or_create(name=name, defaults=extra)

        # Priorities
        pris = [
            ("Critique", 5, {"color": "#DC2626", "sla_hours": 2}),
            ("Élevée", 4, {"color": "#EA580C", "sla_hours": 4}),
            ("Moyenne", 3, {"color": "#D97706", "sla_hours": 24}),
            ("Faible", 2, {"color": "#16A34A", "sla_hours": 72}),
        ]
        for name, level, extra in pris:
            Priority.objects.get_or_create(name=name, defaults={"level": level, **extra})

        # Statuses
        stats = [
            ("Ouvert", {"description": "Ticket nouvellement créé", "is_final": False, "color": "#3B82F6"}),
            ("En cours", {"description": "Ticket en cours de traitement", "is_final": False, "color": "#F59E0B"}),
            ("Fermé", {"description": "Ticket fermé", "is_final": True, "color": "#10B981"}),
        ]
        for name, extra in stats:
            Status.objects.get_or_create(name=name, defaults=extra)

        # Channels (tickets app)
        chans = [
            ("Portail Web", "web"),
            ("Email SMTP", "email"),
            ("SMS Twilio", "sms"),
            ("WhatsApp Business", "whatsapp"),
            ("Téléphone", "phone"),
        ]
        for name, ctype in chans:
            Channel.objects.get_or_create(name=name, defaults={"type": ctype, "is_active": True})

        # Demo tickets
        try:
            admin = get_user_model().objects.filter(username="admin").first()
        except Exception:
            admin = None

        status_open = Status.objects.filter(name="Ouvert").first()
        cat_info = Category.objects.filter(name="Information").first()
        pri_med = Priority.objects.filter(name="Moyenne").first()
        ch_web = Channel.objects.filter(name="Portail Web").first()

        created = 0
        for i in range(3):
            title = f"Ticket de démo #{i+1}"
            if not Ticket.objects.filter(title=title).exists():
                Ticket.objects.create(
                    title=title,
                    content="Créé par seed_tickets_basics",
                    category=cat_info,
                    priority=pri_med,
                    status=status_open,
                    channel=ch_web,
                    created_by=admin,
                )
                created += 1

        self.stdout.write(self.style.SUCCESS(
            f"Seeding done. Categories={Category.objects.count()} Priorities={Priority.objects.count()} "
            f"Statuses={Status.objects.count()} Channels={Channel.objects.count()} NewTickets={created}"
        ))

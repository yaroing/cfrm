-- Script d'initialisation de la base de données CFRM
-- Ce script crée les données de base nécessaires au fonctionnement de l'application

-- Extension pour les UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Extension pour le chiffrement
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Création des rôles par défaut
INSERT INTO users_role (name, description, permissions, is_psea_authorized, can_escalate, can_assign, can_close, can_view_analytics, created_at) VALUES
('Admin', 'Administrateur système', '["all"]', true, true, true, true, true, NOW()),
('Manager', 'Gestionnaire', '["view_tickets", "edit_tickets", "assign_tickets", "close_tickets", "view_analytics"]', true, true, true, true, true, NOW()),
('Agent', 'Agent de traitement', '["view_tickets", "edit_tickets", "create_responses"]', false, false, false, false, false, NOW()),
('PSEA_Focal_Point', 'Point focal PSEA', '["view_tickets", "edit_tickets", "psea_access", "escalate_tickets"]', true, true, false, false, false, NOW()),
('Viewer', 'Consultant', '["view_tickets", "view_analytics"]', false, false, false, false, true, NOW())
ON CONFLICT (name) DO NOTHING;

-- Création des organisations par défaut
INSERT INTO users_organization (name, code, description, contact_email, is_active, created_at, updated_at) VALUES
('CFRM Platform', 'CFRM', 'Plateforme de feedback communautaire', 'admin@cfrm.org', true, NOW(), NOW()),
('UNICEF', 'UNICEF', 'Fonds des Nations Unies pour l''enfance', 'contact@unicef.org', true, NOW(), NOW()),
('UNHCR', 'UNHCR', 'Haut Commissariat des Nations Unies pour les réfugiés', 'contact@unhcr.org', true, NOW(), NOW()),
('WFP', 'WFP', 'Programme alimentaire mondial', 'contact@wfp.org', true, NOW(), NOW()),
('IFRC', 'IFRC', 'Fédération internationale des Sociétés de la Croix-Rouge et du Croissant-Rouge', 'contact@ifrc.org', true, NOW(), NOW())
ON CONFLICT (name) DO NOTHING;

-- Création des catégories par défaut
INSERT INTO tickets_category (name, description, is_sensitive, requires_escalation, escalation_contact, created_at, updated_at) VALUES
('Information', 'Demande d''information générale', false, false, '', NOW(), NOW()),
('Complaint', 'Plainte générale', false, true, 'complaints@cfrm.org', NOW(), NOW()),
('Request', 'Demande de service', false, false, '', NOW(), NOW()),
('PSEA', 'Protection contre l''exploitation et les abus sexuels', true, true, 'psea@cfrm.org', NOW(), NOW()),
('SEA', 'Exploitation et abus sexuels', true, true, 'sea@cfrm.org', NOW(), NOW()),
('Feedback', 'Retour d''expérience', false, false, '', NOW(), NOW()),
('Suggestion', 'Suggestion d''amélioration', false, false, '', NOW(), NOW()),
('Other', 'Autre', false, false, '', NOW(), NOW())
ON CONFLICT (name) DO NOTHING;

-- Création des priorités par défaut
INSERT INTO tickets_priority (name, level, color, sla_hours, created_at) VALUES
('Critique', 5, '#DC2626', 2, NOW()),
('Élevée', 4, '#EA580C', 4, NOW()),
('Moyenne', 3, '#D97706', 24, NOW()),
('Faible', 2, '#16A34A', 72, NOW()),
('Information', 1, '#2563EB', 168, NOW())
ON CONFLICT (name) DO NOTHING;

-- Création des statuts par défaut
INSERT INTO tickets_status (name, description, is_final, color, created_at) VALUES
('Ouvert', 'Ticket nouvellement créé', false, '#3B82F6', NOW()),
('En cours', 'Ticket en cours de traitement', false, '#F59E0B', NOW()),
('En attente', 'Ticket en attente de réponse', false, '#8B5CF6', NOW()),
('Escaladé', 'Ticket escaladé vers un niveau supérieur', false, '#EF4444', NOW()),
('Fermé', 'Ticket fermé', true, '#10B981', NOW()),
('Annulé', 'Ticket annulé', true, '#6B7280', NOW())
ON CONFLICT (name) DO NOTHING;

-- Création des canaux par défaut
INSERT INTO channels_channelconfiguration (name, type, is_active, configuration, created_at, updated_at) VALUES
('SMS Twilio', 'sms', true, '{"provider": "twilio", "phone_number": "+1234567890"}', NOW(), NOW()),
('WhatsApp Business', 'whatsapp', true, '{"provider": "whatsapp", "phone_number_id": "123456789"}', NOW(), NOW()),
('Email SMTP', 'email', true, '{"provider": "smtp", "host": "smtp.gmail.com", "port": 587}', NOW(), NOW()),
('Portail Web', 'web', true, '{"provider": "web", "url": "https://cfrm.org"}', NOW(), NOW()),
('Téléphone', 'phone', true, '{"provider": "phone", "number": "+1234567890"}', NOW(), NOW())
ON CONFLICT (name) DO NOTHING;

-- Création des modèles de messages par défaut
INSERT INTO channels_messagetemplate (name, channel_id, template_type, subject, content, language, variables, is_active, created_at, updated_at) VALUES
('Confirmation SMS', (SELECT id FROM channels_channelconfiguration WHERE type='sms' LIMIT 1), 'confirmation', '', 'Merci pour votre message. Votre ticket #{ticket_id} a été reçu et sera traité dans les plus brefs délais.', 'fr', '["ticket_id", "title", "category"]', true, NOW(), NOW()),
('Confirmation WhatsApp', (SELECT id FROM channels_channelconfiguration WHERE type='whatsapp' LIMIT 1), 'confirmation', '', 'Merci pour votre message. Votre ticket #{ticket_id} a été reçu et sera traité dans les plus brefs délais.', 'fr', '["ticket_id", "title", "category"]', true, NOW(), NOW()),
('Confirmation Email', (SELECT id FROM channels_channelconfiguration WHERE type='email' LIMIT 1), 'confirmation', 'Confirmation de réception - Ticket #{ticket_id}', 'Bonjour,\n\nNous avons bien reçu votre message concernant : {title}\n\nVotre ticket #{ticket_id} a été enregistré dans la catégorie "{category}" avec la priorité "{priority}".\n\nNous vous répondrons dans les plus brefs délais.\n\nCordialement,\nL''équipe CFRM', 'fr', '["ticket_id", "title", "category", "priority"]', true, NOW(), NOW()),
('Réponse SMS', (SELECT id FROM channels_channelconfiguration WHERE type='sms' LIMIT 1), 'response', '', 'Réponse à votre ticket #{ticket_id} : {response_content}', 'fr', '["ticket_id", "response_content", "responder"]', true, NOW(), NOW()),
('Réponse WhatsApp', (SELECT id FROM channels_channelconfiguration WHERE type='whatsapp' LIMIT 1), 'response', '', 'Réponse à votre ticket #{ticket_id} :\n\n{response_content}\n\nRépondant : {responder}', 'fr', '["ticket_id", "response_content", "responder"]', true, NOW(), NOW()),
('Réponse Email', (SELECT id FROM channels_channelconfiguration WHERE type='email' LIMIT 1), 'response', 'Réponse à votre ticket #{ticket_id}', 'Bonjour,\n\nVoici la réponse à votre ticket #{ticket_id} :\n\n{response_content}\n\nRépondant : {responder}\n\nCordialement,\nL''équipe CFRM', 'fr', '["ticket_id", "response_content", "responder"]', true, NOW(), NOW()),
('Escalade PSEA', (SELECT id FROM channels_channelconfiguration WHERE type='email' LIMIT 1), 'escalation', 'URGENT - Escalade PSEA - Ticket #{ticket_id}', 'URGENT : Ticket PSEA escaladé\n\nTicket #{ticket_id}\nTitre : {title}\nContenu : {content}\n\nAction requise immédiatement.', 'fr', '["ticket_id", "title", "content"]', true, NOW(), NOW())
ON CONFLICT (name, channel_id, template_type, language) DO NOTHING;

-- Création des métriques par défaut
INSERT INTO analytics_metric (name, description, metric_type, query, unit, target_value, warning_threshold, critical_threshold, is_active, created_at, updated_at) VALUES
('Tickets créés', 'Nombre de tickets créés par jour', 'counter', '{"model": "tickets.Ticket", "field": "created_at"}', 'tickets', 100, 150, 200, true, NOW(), NOW()),
('Tickets fermés', 'Nombre de tickets fermés par jour', 'counter', '{"model": "tickets.Ticket", "field": "closed_at"}', 'tickets', 100, 80, 50, true, NOW(), NOW()),
('Temps de réponse moyen', 'Temps de réponse moyen en heures', 'gauge', '{"model": "tickets.Ticket", "calculation": "avg_response_time"}', 'heures', 24, 48, 72, true, NOW(), NOW()),
('Taux de satisfaction', 'Taux de satisfaction moyen', 'gauge', '{"model": "tickets.Feedback", "field": "satisfaction_rating"}', '%', 4.0, 3.0, 2.0, true, NOW(), NOW()),
('Tickets en retard', 'Nombre de tickets en retard de SLA', 'counter', '{"model": "tickets.Ticket", "filter": "is_overdue"}', 'tickets', 0, 5, 10, true, NOW(), NOW())
ON CONFLICT (name) DO NOTHING;

-- Création d'un utilisateur administrateur par défaut
INSERT INTO users_user (id, username, email, first_name, last_name, is_staff, is_superuser, is_active, is_verified, organization_id, role_id, created_at, updated_at) VALUES
(uuid_generate_v4(), 'admin', 'admin@cfrm.org', 'Admin', 'CFRM', true, true, true, true, 
 (SELECT id FROM users_organization WHERE code='CFRM' LIMIT 1),
 (SELECT id FROM users_role WHERE name='Admin' LIMIT 1),
 NOW(), NOW())
ON CONFLICT (username) DO NOTHING;

-- Création d'un tableau de bord par défaut
INSERT INTO analytics_dashboard (name, description, layout, widgets, filters, is_public, is_default, created_by_id, created_at, updated_at) VALUES
('Tableau de bord principal', 'Tableau de bord principal de la plateforme CFRM', 
 '{"columns": 3, "rows": 4}', 
 '[{"type": "metric", "title": "Tickets ouverts", "position": {"x": 0, "y": 0, "w": 1, "h": 1}}, {"type": "metric", "title": "Tickets fermés", "position": {"x": 1, "y": 0, "w": 1, "h": 1}}, {"type": "metric", "title": "Temps de réponse", "position": {"x": 2, "y": 0, "w": 1, "h": 1}}, {"type": "chart", "title": "Tickets par statut", "position": {"x": 0, "y": 1, "w": 2, "h": 2}}, {"type": "chart", "title": "Tickets par canal", "position": {"x": 2, "y": 1, "w": 1, "h": 2}}]',
 '{"date_range": "last_30_days"}', true, true, 
 (SELECT id FROM users_user WHERE username='admin' LIMIT 1), NOW(), NOW())
ON CONFLICT (name) DO NOTHING;

-- Création d'un rapport template par défaut
INSERT INTO analytics_reporttemplate (name, description, report_type, query_filters, chart_config, export_formats, is_active, is_public, created_by_id, created_at, updated_at) VALUES
('Rapport mensuel des tickets', 'Rapport mensuel standard des tickets', 'tickets_summary',
 '{"group_by": ["category", "status", "channel"], "date_field": "created_at"}',
 '{"charts": [{"type": "bar", "title": "Tickets par catégorie"}, {"type": "pie", "title": "Répartition par statut"}]}',
 '["csv", "excel", "pdf"]', true, true,
 (SELECT id FROM users_user WHERE username='admin' LIMIT 1), NOW(), NOW())
ON CONFLICT (name) DO NOTHING;

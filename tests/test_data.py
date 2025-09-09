"""
Jeux de données fictifs pour les tests de la plateforme CFRM
Plateforme de Feedback Communautaire pour le secteur humanitaire
"""
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

class TestDataGenerator:
    """Générateur de données de test pour la plateforme CFRM humanitaire"""
    
    def __init__(self):
        # Langues supportées dans les contextes humanitaires
        self.languages = ['fr', 'en', 'ar', 'es', 'sw', 'am', 'so', 'ti']
        
        # Catégories spécifiques au secteur humanitaire (selon le modèle CFRM)
        self.categories = [
            'Information', 'Complaint', 'Request', 'PSEA', 'SEA', 
            'Feedback', 'Suggestion', 'Other'
        ]
        
        # Priorités selon le modèle CFRM
        self.priorities = ['Critique', 'Élevée', 'Moyenne', 'Faible', 'Information']
        
        # Canaux de communication humanitaire
        self.channels = ['sms', 'whatsapp', 'web', 'email', 'phone', 'paper']
        
        # Sentiments pour l'analyse
        self.sentiments = ['Positive', 'Negative', 'Neutral']
        
        # Contextes humanitaires spécifiques
        self.humanitarian_contexts = [
            'refugee_camp', 'displacement', 'emergency_response', 'recovery', 
            'development', 'protection', 'health', 'education', 'shelter', 'food_security'
        ]
        
        # Types de populations affectées
        self.affected_populations = [
            'refugees', 'idps', 'returnees', 'host_community', 'vulnerable_groups',
            'women_children', 'elderly', 'persons_with_disabilities', 'minorities'
        ]
        
    def generate_sms_messages(self, count: int = 100) -> List[Dict[str, Any]]:
        """Génère des messages SMS de test pour le contexte humanitaire"""
        messages = []
        
        # Messages en français - contexte humanitaire
        french_templates = [
            "Bonjour, j'ai besoin d'aide pour {service}",
            "URGENT: Problème avec {issue} dans le camp",
            "Merci pour {service}, {compliment}",
            "Comment puis-je {action} ?",
            "Je ne reçois pas {service}",
            "Excellent travail avec {program}",
            "Problème signalé: {issue_description}",
            "Pouvez-vous m'aider avec {question} ?",
            "Plainte concernant {complaint_subject}",
            "Demande d'information sur {info_request}"
        ]
        
        # Messages en anglais - contexte humanitaire
        english_templates = [
            "Hello, I need help with {service}",
            "URGENT: Problem with {issue} in the camp",
            "Thank you for {service}, {compliment}",
            "How can I {action}?",
            "I am not receiving {service}",
            "Great work with {program}",
            "Issue reported: {issue_description}",
            "Can you help me with {question}?",
            "Complaint about {complaint_subject}",
            "Information request about {info_request}"
        ]
        
        # Messages en arabe - contexte humanitaire
        arabic_templates = [
            "مرحبا، أحتاج مساعدة مع {service}",
            "عاجل: مشكلة مع {issue} في المخيم",
            "شكرا لكم على {service}، {compliment}",
            "كيف يمكنني {action}؟",
            "لا أتلقى {service}",
            "عمل رائع مع {program}",
            "تم الإبلاغ عن مشكلة: {issue_description}",
            "هل يمكنكم مساعدتي مع {question}؟"
        ]
        
        # Vocabulaire humanitaire spécifique
        services = ["distribution alimentaire", "soins médicaux", "eau potable", "abri", "éducation", "protection"]
        issues = ["distribution", "sécurité", "hygiène", "accès", "transport", "communication"]
        compliments = ["très efficace", "excellent", "parfait", "génial", "professionnel"]
        actions = ["m'inscrire", "obtenir un rendez-vous", "changer d'emplacement", "contacter un responsable"]
        problems = ["recevoir l'aide", "accéder au service", "obtenir des informations", "me déplacer"]
        programs = ["l'aide alimentaire", "les soins de santé", "l'éducation", "la protection"]
        issue_descriptions = ["eau contaminée", "distribution inégale", "sécurité insuffisante", "attente trop longue"]
        questions = ["mon dossier", "les prochaines distributions", "les services disponibles", "mes droits"]
        complaint_subjects = ["le personnel", "la qualité des services", "les délais", "l'accès"]
        info_requests = ["les critères d'éligibilité", "les prochaines activités", "les procédures", "les contacts"]
        
        for i in range(count):
            language = random.choice(self.languages)
            channel = 'sms'
            
            if language == 'fr':
                template = random.choice(french_templates)
                service = random.choice(services)
                issue = random.choice(issues)
                compliment = random.choice(compliments)
                action = random.choice(actions)
                problem = random.choice(problems)
                program = random.choice(programs)
                issue_description = random.choice(issue_descriptions)
                question = random.choice(questions)
                complaint_subject = random.choice(complaint_subjects)
                info_request = random.choice(info_requests)
            elif language == 'ar':
                template = random.choice(arabic_templates)
                service = random.choice(["توزيع الطعام", "الرعاية الطبية", "الماء الصالح للشرب", "المأوى", "التعليم", "الحماية"])
                issue = random.choice(["التوزيع", "الأمان", "النظافة", "الوصول", "النقل", "التواصل"])
                compliment = random.choice(["فعال جداً", "ممتاز", "مثالي", "رائع", "مهني"])
                action = random.choice(["التسجيل", "الحصول على موعد", "تغيير الموقع", "الاتصال بمسؤول"])
                problem = random.choice(["تلقي المساعدة", "الوصول للخدمة", "الحصول على معلومات", "الانتقال"])
                program = random.choice(["المساعدة الغذائية", "الرعاية الصحية", "التعليم", "الحماية"])
                issue_description = random.choice(["ماء ملوث", "توزيع غير متساوي", "أمان غير كافي", "انتظار طويل"])
                question = random.choice(["ملفي", "التوزيعات القادمة", "الخدمات المتاحة", "حقوقي"])
            else:  # anglais
                template = random.choice(english_templates)
                service = random.choice(["food distribution", "medical care", "clean water", "shelter", "education", "protection"])
                issue = random.choice(["distribution", "security", "hygiene", "access", "transport", "communication"])
                compliment = random.choice(["very efficient", "excellent", "perfect", "great", "professional"])
                action = random.choice(["register", "get an appointment", "change location", "contact a manager"])
                problem = random.choice(["receive assistance", "access the service", "get information", "move around"])
                program = random.choice(["food assistance", "healthcare", "education", "protection"])
                issue_description = random.choice(["contaminated water", "uneven distribution", "insufficient security", "too long wait"])
                question = random.choice(["my file", "next distributions", "available services", "my rights"])
                complaint_subject = random.choice(["staff", "service quality", "delays", "access"])
                info_request = random.choice(["eligibility criteria", "next activities", "procedures", "contacts"])
            
            message_text = template.format(
                service=service,
                issue=issue,
                compliment=compliment,
                action=action,
                problem=problem,
                program=program,
                issue_description=issue_description,
                question=question,
                complaint_subject=complaint_subject,
                info_request=info_request
            )
            
            # Ajouter des variations contextuelles humanitaires
            if random.random() < 0.3:
                message_text += f" - Famille {random.randint(1, 10)} personnes"
            if random.random() < 0.2:
                message_text += " - URGENT"
            if random.random() < 0.1:
                message_text += " 🙏"
            if random.random() < 0.15:
                message_text += f" - Zone {random.choice(['A', 'B', 'C', 'D'])}"
                
            # Informations contextuelles humanitaires
            humanitarian_context = random.choice(self.humanitarian_contexts)
            affected_population = random.choice(self.affected_populations)
            
            messages.append({
                'id': f'sms_{i+1:03d}',
                'text': message_text,
                'language': language,
                'channel': channel,
                'phone_number': self._generate_phone_number(),
                'timestamp': self._random_timestamp(),
                'humanitarian_context': humanitarian_context,
                'affected_population': affected_population,
                'is_psea_related': self._is_psea_related(message_text),
                'requires_escalation': self._requires_escalation(message_text),
                'expected_category': self._predict_category(message_text, language),
                'expected_priority': self._predict_priority(message_text),
                'expected_sentiment': self._predict_sentiment(message_text)
            })
            
        return messages
    
    def generate_web_forms(self, count: int = 50) -> List[Dict[str, Any]]:
        """Génère des formulaires web de test pour le contexte humanitaire"""
        forms = []
        
        # Sujets spécifiques au secteur humanitaire
        subjects = [
            "Problème avec la distribution alimentaire",
            "Demande d'information sur les services",
            "Question sur mon éligibilité",
            "Problème d'accès aux soins médicaux",
            "Suggestion d'amélioration des services",
            "Plainte concernant le personnel",
            "Félicitations pour l'aide reçue",
            "Demande d'assistance technique",
            "Signalement d'incident de sécurité",
            "Demande de réinstallation"
        ]
        
        # Descriptions contextuelles humanitaires
        descriptions = [
            "Je n'ai pas reçu ma ration alimentaire cette semaine. Ma famille de 6 personnes n'a rien à manger. Pouvez-vous vérifier ?",
            "Comment puis-je m'inscrire pour les soins médicaux ? J'ai des enfants malades qui ont besoin de soins urgents.",
            "Je ne comprends pas pourquoi ma demande d'aide a été refusée. Pouvez-vous m'expliquer les critères d'éligibilité ?",
            "L'accès à l'eau potable dans notre zone est très difficile. Il n'y a qu'un seul point d'eau pour 200 familles.",
            "Je suggère d'organiser les distributions plus tôt le matin pour éviter les longues files d'attente sous le soleil.",
            "Le personnel de distribution n'est pas respectueux avec les femmes. Il y a des commentaires inappropriés.",
            "Merci pour l'excellent travail de votre équipe. L'aide reçue a vraiment changé notre situation.",
            "J'ai des difficultés à utiliser l'application mobile pour suivre mes dossiers. Pouvez-vous m'aider ?",
            "J'ai été témoin d'un incident de sécurité près du point de distribution. Il faut renforcer la sécurité.",
            "Ma famille et moi souhaitons être réinstallés dans une autre zone. Comment procéder ?"
        ]
        
        for i in range(count):
            subject = random.choice(subjects)
            description = random.choice(descriptions)
            
            form = {
                'id': f'web_{i+1:03d}',
                'subject': subject,
                'description': description,
                'category': random.choice(self.categories),
                'priority': random.choice(self.priorities),
                'user_email': f'beneficiary{i+1}@example.com',
                'user_name': f'Bénéficiaire {i+1}',
                'user_phone': self._generate_phone_number(),
                'user_location': f'Zone {random.choice(["A", "B", "C", "D"])} - Secteur {random.randint(1, 10)}',
                'family_size': random.randint(1, 12),
                'vulnerability_status': random.choice(['vulnerable', 'not_vulnerable', 'unknown']),
                'language': 'fr',
                'channel': 'web',
                'has_attachment': random.random() < 0.3,
                'attachment_type': random.choice(['image', 'document', 'video']) if random.random() < 0.3 else None,
                'timestamp': self._random_timestamp(),
                'humanitarian_context': random.choice(self.humanitarian_contexts),
                'affected_population': random.choice(self.affected_populations),
                'is_psea_related': self._is_psea_related(description),
                'requires_escalation': self._requires_escalation(description),
                'expected_category': self._predict_category(subject + " " + description, 'fr'),
                'expected_priority': self._predict_priority(description),
                'expected_sentiment': self._predict_sentiment(description)
            }
            forms.append(form)
            
        return forms
    
    def generate_messaging_messages(self, count: int = 75) -> List[Dict[str, Any]]:
        """Génère des messages de messagerie instantanée pour le contexte humanitaire"""
        messages = []
        
        platforms = ['whatsapp', 'telegram', 'discord', 'slack']
        
        # Messages courts typiques des messageries humanitaires
        short_messages = [
            "Salut, j'ai un problème avec l'aide",
            "Help! Pas de nourriture",
            "Merci pour l'aide 👍",
            "Comment s'inscrire ?",
            "Ça marche pas",
            "Super service !",
            "Problème ici",
            "Question rapide sur mon dossier"
        ]
        
        # Messages avec emojis - contexte humanitaire
        emoji_messages = [
            "😊 L'aide est arrivée !",
            "😡 Très déçu par le service",
            "🤔 Comment obtenir de l'aide ?",
            "👍 Distribution parfaite !",
            "❌ Pas reçu ma ration",
            "✅ Problème résolu !",
            "🚀 Excellent travail !",
            "💔 Famille en difficulté"
        ]
        
        # Messages avec médias - contexte humanitaire
        media_messages = [
            "Voici une photo du problème d'eau",
            "Regardez cette image de la distribution",
            "J'ai joint un document de ma famille",
            "Photo du point d'eau cassé",
            "Vidéo de l'incident de sécurité"
        ]
        
        for i in range(count):
            platform = random.choice(platforms)
            
            if random.random() < 0.4:
                text = random.choice(short_messages)
            elif random.random() < 0.7:
                text = random.choice(emoji_messages)
            else:
                text = random.choice(media_messages)
            
            message = {
                'id': f'msg_{i+1:03d}',
                'text': text,
                'platform': platform,
                'channel': platform,
                'user_id': f'user_{random.randint(1000, 9999)}',
                'username': f'user{random.randint(1, 100)}',
                'has_media': random.random() < 0.3,
                'media_type': random.choice(['image', 'video', 'document', 'audio']) if random.random() < 0.3 else None,
                'is_group': random.random() < 0.2,
                'group_name': f'Groupe {random.randint(1, 10)}' if random.random() < 0.2 else None,
                'language': random.choice(['fr', 'en']),
                'timestamp': self._random_timestamp(),
                'expected_category': self._predict_category(text, 'fr'),
                'expected_priority': self._predict_priority(text),
                'expected_sentiment': self._predict_sentiment(text)
            }
            messages.append(message)
            
        return messages
    
    def generate_performance_test_data(self) -> Dict[str, Any]:
        """Génère des données pour les tests de performance"""
        return {
            'load_test_scenarios': [
                {
                    'name': 'Charge normale',
                    'messages_per_minute': 100,
                    'duration_minutes': 60,
                    'expected_response_time': 2.0
                },
                {
                    'name': 'Charge élevée',
                    'messages_per_minute': 500,
                    'duration_minutes': 30,
                    'expected_response_time': 5.0
                },
                {
                    'name': 'Pic de charge',
                    'messages_per_minute': 1000,
                    'duration_minutes': 10,
                    'expected_response_time': 10.0
                }
            ],
            'stress_test_scenarios': [
                {
                    'name': 'Test de stress',
                    'concurrent_users': 1000,
                    'messages_per_user': 10,
                    'duration_minutes': 15
                }
            ]
        }
    
    def _random_timestamp(self) -> str:
        """Génère un timestamp aléatoire dans les 30 derniers jours"""
        now = datetime.now()
        random_days = random.randint(0, 30)
        random_hours = random.randint(0, 23)
        random_minutes = random.randint(0, 59)
        
        timestamp = now - timedelta(days=random_days, hours=random_hours, minutes=random_minutes)
        return timestamp.isoformat()
    
    def _predict_category(self, text: str, language: str) -> str:
        """Prédit la catégorie basée sur le contenu du message"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['bug', 'erreur', 'problème', 'ça marche pas', 'broken']):
            return 'Bug'
        elif any(word in text_lower for word in ['demande', 'suggestion', 'feature', 'fonctionnalité']):
            return 'Feature Request'
        elif any(word in text_lower for word in ['question', 'comment', 'help', 'aide']):
            return 'Question'
        elif any(word in text_lower for word in ['merci', 'parfait', 'excellent', 'super']):
            return 'Praise'
        elif any(word in text_lower for word in ['facture', 'billing', 'paiement', 'payment']):
            return 'Billing'
        else:
            return random.choice(self.categories)
    
    def _predict_priority(self, text: str) -> str:
        """Prédit la priorité basée sur le contenu du message"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['urgent', 'critique', 'critical', 'bloqué', 'blocked']):
            return 'Critical'
        elif any(word in text_lower for word in ['important', 'rapide', 'quick', 'asap']):
            return 'High'
        elif any(word in text_lower for word in ['normal', 'standard', 'moyen']):
            return 'Medium'
        else:
            return 'Low'
    
    def _predict_sentiment(self, text: str) -> str:
        """Prédit le sentiment basé sur le contenu du message"""
        text_lower = text.lower()
        
        positive_words = ['merci', 'parfait', 'excellent', 'super', 'génial', '👍', '😊', '✅', 'aide', 'bien', 'bon']
        negative_words = ['problème', 'bug', 'erreur', 'déçu', '😡', '❌', '💔', 'ça marche pas', 'difficile', 'mal']
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return 'Positive'
        elif negative_count > positive_count:
            return 'Negative'
        else:
            return 'Neutral'
    
    def _generate_phone_number(self) -> str:
        """Génère un numéro de téléphone réaliste pour différents pays"""
        country_codes = ['+33', '+1', '+44', '+49', '+39', '+34', '+90', '+966', '+20', '+27']
        country_code = random.choice(country_codes)
        number = ''.join([str(random.randint(0, 9)) for _ in range(9)])
        return f"{country_code}{number}"
    
    def _is_psea_related(self, text: str) -> bool:
        """Détermine si le message est lié à PSEA/SEA"""
        text_lower = text.lower()
        psea_keywords = [
            'abus', 'exploitation', 'sexuel', 'harcèlement', 'violence', 'inapproprié',
            'respect', 'dignité', 'protection', 'sécurité', 'personnel', 'comportement'
        ]
        return any(keyword in text_lower for keyword in psea_keywords)
    
    def _requires_escalation(self, text: str) -> bool:
        """Détermine si le message nécessite une escalade"""
        text_lower = text.lower()
        escalation_keywords = [
            'urgent', 'critique', 'grave', 'sécurité', 'abus', 'exploitation',
            'plainte', 'réclamation', 'escalade', 'manager', 'responsable'
        ]
        return any(keyword in text_lower for keyword in escalation_keywords)

# Exemple d'utilisation
if __name__ == "__main__":
    generator = TestDataGenerator()
    
    print("=== Génération des données de test ===")
    
    # Générer les données
    sms_data = generator.generate_sms_messages(50)
    web_data = generator.generate_web_forms(25)
    msg_data = generator.generate_messaging_messages(25)
    perf_data = generator.generate_performance_test_data()
    
    print(f"SMS Messages: {len(sms_data)}")
    print(f"Web Forms: {len(web_data)}")
    print(f"Messaging: {len(msg_data)}")
    
    # Afficher quelques exemples
    print("\n=== Exemples de données ===")
    print("SMS:", sms_data[0])
    print("Web:", web_data[0])
    print("Messaging:", msg_data[0])

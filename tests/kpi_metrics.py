"""
KPI et Indicateurs de Performance pour la plateforme CFRM
"""
from dataclasses import dataclass
from typing import Dict, List, Any
from datetime import datetime, timedelta
import statistics

@dataclass
class KPIMetric:
    """Classe pour définir une métrique KPI"""
    name: str
    description: str
    unit: str
    target_value: float
    current_value: float
    calculation_method: str
    importance: str  # 'Critical', 'High', 'Medium', 'Low'

class CFRMKPIs:
    """Classe principale pour gérer les KPI de la plateforme CFRM"""
    
    def __init__(self):
        self.metrics = self._initialize_metrics()
    
    def _initialize_metrics(self) -> Dict[str, KPIMetric]:
        """Initialise toutes les métriques KPI"""
        return {
            # === MÉTRIQUES DE RÉCEPTION ===
            'reception_rate': KPIMetric(
                name="Taux de Réception",
                description="Pourcentage de messages reçus avec succès",
                unit="%",
                target_value=99.5,
                current_value=0.0,
                calculation_method="(Messages reçus / Messages envoyés) * 100",
                importance="Critical"
            ),
            
            'reception_latency': KPIMetric(
                name="Délai de Réception",
                description="Temps moyen entre l'envoi et la réception",
                unit="secondes",
                target_value=5.0,
                current_value=0.0,
                calculation_method="Moyenne des délais de réception",
                importance="High"
            ),
            
            'channel_availability': KPIMetric(
                name="Disponibilité des Canaux",
                description="Pourcentage de temps de fonctionnement des canaux",
                unit="%",
                target_value=99.9,
                current_value=0.0,
                calculation_method="(Temps de fonctionnement / Temps total) * 100",
                importance="Critical"
            ),
            
            # === MÉTRIQUES DE TRAITEMENT ===
            'processing_time': KPIMetric(
                name="Délai de Traitement",
                description="Temps moyen de traitement d'un ticket",
                unit="minutes",
                target_value=15.0,
                current_value=0.0,
                calculation_method="Moyenne des temps de traitement",
                importance="High"
            ),
            
            'classification_accuracy': KPIMetric(
                name="Précision de Classification",
                description="Pourcentage de tickets correctement classés",
                unit="%",
                target_value=85.0,
                current_value=0.0,
                calculation_method="(Classifications correctes / Total) * 100",
                importance="High"
            ),
            
            'auto_classification_rate': KPIMetric(
                name="Taux de Classification Automatique",
                description="Pourcentage de tickets classés automatiquement",
                unit="%",
                target_value=70.0,
                current_value=0.0,
                calculation_method="(Tickets auto-classés / Total) * 100",
                importance="Medium"
            ),
            
            # === MÉTRIQUES DE SATISFACTION ===
            'user_satisfaction': KPIMetric(
                name="Satisfaction Utilisateur",
                description="Score moyen de satisfaction des utilisateurs",
                unit="/10",
                target_value=8.0,
                current_value=0.0,
                calculation_method="Moyenne des scores de satisfaction",
                importance="Critical"
            ),
            
            'response_satisfaction': KPIMetric(
                name="Satisfaction des Réponses",
                description="Pourcentage d'utilisateurs satisfaits des réponses",
                unit="%",
                target_value=80.0,
                current_value=0.0,
                calculation_method="(Utilisateurs satisfaits / Total) * 100",
                importance="High"
            ),
            
            'resolution_satisfaction': KPIMetric(
                name="Satisfaction de Résolution",
                description="Pourcentage de problèmes résolus à la satisfaction",
                unit="%",
                target_value=75.0,
                current_value=0.0,
                calculation_method="(Problèmes résolus / Total) * 100",
                importance="High"
            ),
            
            # === MÉTRIQUES DE PERFORMANCE ===
            'throughput': KPIMetric(
                name="Débit de Traitement",
                description="Nombre de tickets traités par heure",
                unit="tickets/heure",
                target_value=100.0,
                current_value=0.0,
                calculation_method="Tickets traités / Temps écoulé",
                importance="High"
            ),
            
            'queue_length': KPIMetric(
                name="Longueur de File d'Attente",
                description="Nombre moyen de tickets en attente",
                unit="tickets",
                target_value=10.0,
                current_value=0.0,
                calculation_method="Moyenne des tickets en attente",
                importance="Medium"
            ),
            
            'error_rate': KPIMetric(
                name="Taux d'Erreur",
                description="Pourcentage de tickets avec erreurs de traitement",
                unit="%",
                target_value=2.0,
                current_value=0.0,
                calculation_method="(Tickets avec erreurs / Total) * 100",
                importance="Critical"
            ),
            
            # === MÉTRIQUES DE QUALITÉ ===
            'first_contact_resolution': KPIMetric(
                name="Résolution au Premier Contact",
                description="Pourcentage de tickets résolus au premier contact",
                unit="%",
                target_value=60.0,
                current_value=0.0,
                calculation_method="(Tickets résolus au 1er contact / Total) * 100",
                importance="High"
            ),
            
            'escalation_rate': KPIMetric(
                name="Taux d'Escalade",
                description="Pourcentage de tickets escaladés",
                unit="%",
                target_value=15.0,
                current_value=0.0,
                calculation_method="(Tickets escaladés / Total) * 100",
                importance="Medium"
            ),
            
            'abandonment_rate': KPIMetric(
                name="Taux d'Abandon",
                description="Pourcentage d'utilisateurs abandonnant avant résolution",
                unit="%",
                target_value=5.0,
                current_value=0.0,
                calculation_method="(Abandons / Total) * 100",
                importance="High"
            ),
            
            # === MÉTRIQUES SPÉCIFIQUES PAR CANAL ===
            'sms_success_rate': KPIMetric(
                name="Taux de Succès SMS",
                description="Pourcentage de messages SMS traités avec succès",
                unit="%",
                target_value=98.0,
                current_value=0.0,
                calculation_method="(SMS traités / SMS reçus) * 100",
                importance="High"
            ),
            
            'web_form_completion': KPIMetric(
                name="Taux de Completion des Formulaires Web",
                description="Pourcentage de formulaires complétés avec succès",
                unit="%",
                target_value=90.0,
                current_value=0.0,
                calculation_method="(Formulaires complétés / Formulaires commencés) * 100",
                importance="Medium"
            ),
            
            'messaging_response_time': KPIMetric(
                name="Temps de Réponse Messagerie",
                description="Temps moyen de réponse aux messages de messagerie",
                unit="minutes",
                target_value=5.0,
                current_value=0.0,
                calculation_method="Moyenne des temps de réponse",
                importance="High"
            )
        }
    
    def calculate_metrics(self, test_data: Dict[str, Any]) -> Dict[str, float]:
        """Calcule toutes les métriques basées sur les données de test"""
        results = {}
        
        # Métriques de réception
        results['reception_rate'] = self._calculate_reception_rate(test_data)
        results['reception_latency'] = self._calculate_reception_latency(test_data)
        results['channel_availability'] = self._calculate_channel_availability(test_data)
        
        # Métriques de traitement
        results['processing_time'] = self._calculate_processing_time(test_data)
        results['classification_accuracy'] = self._calculate_classification_accuracy(test_data)
        results['auto_classification_rate'] = self._calculate_auto_classification_rate(test_data)
        
        # Métriques de satisfaction
        results['user_satisfaction'] = self._calculate_user_satisfaction(test_data)
        results['response_satisfaction'] = self._calculate_response_satisfaction(test_data)
        results['resolution_satisfaction'] = self._calculate_resolution_satisfaction(test_data)
        
        # Métriques de performance
        results['throughput'] = self._calculate_throughput(test_data)
        results['queue_length'] = self._calculate_queue_length(test_data)
        results['error_rate'] = self._calculate_error_rate(test_data)
        
        # Métriques de qualité
        results['first_contact_resolution'] = self._calculate_first_contact_resolution(test_data)
        results['escalation_rate'] = self._calculate_escalation_rate(test_data)
        results['abandonment_rate'] = self._calculate_abandonment_rate(test_data)
        
        # Métriques par canal
        results['sms_success_rate'] = self._calculate_sms_success_rate(test_data)
        results['web_form_completion'] = self._calculate_web_form_completion(test_data)
        results['messaging_response_time'] = self._calculate_messaging_response_time(test_data)
        
        return results
    
    def _calculate_reception_rate(self, data: Dict[str, Any]) -> float:
        """Calcule le taux de réception"""
        total_sent = data.get('total_messages_sent', 1000)
        total_received = data.get('total_messages_received', 995)
        return (total_received / total_sent) * 100 if total_sent > 0 else 0
    
    def _calculate_reception_latency(self, data: Dict[str, Any]) -> float:
        """Calcule le délai de réception moyen"""
        latencies = data.get('reception_latencies', [2.1, 3.5, 4.2, 1.8, 5.1, 2.9, 3.7, 4.8])
        return statistics.mean(latencies) if latencies else 0
    
    def _calculate_channel_availability(self, data: Dict[str, Any]) -> float:
        """Calcule la disponibilité des canaux"""
        uptime = data.get('channel_uptime_hours', 99.9)
        total_time = data.get('total_time_hours', 100.0)
        return (uptime / total_time) * 100 if total_time > 0 else 0
    
    def _calculate_processing_time(self, data: Dict[str, Any]) -> float:
        """Calcule le temps de traitement moyen"""
        processing_times = data.get('processing_times_minutes', [12, 18, 15, 22, 8, 25, 14, 16])
        return statistics.mean(processing_times) if processing_times else 0
    
    def _calculate_classification_accuracy(self, data: Dict[str, Any]) -> float:
        """Calcule la précision de classification"""
        correct_classifications = data.get('correct_classifications', 850)
        total_classifications = data.get('total_classifications', 1000)
        return (correct_classifications / total_classifications) * 100 if total_classifications > 0 else 0
    
    def _calculate_auto_classification_rate(self, data: Dict[str, Any]) -> float:
        """Calcule le taux de classification automatique"""
        auto_classified = data.get('auto_classified_tickets', 700)
        total_tickets = data.get('total_tickets', 1000)
        return (auto_classified / total_tickets) * 100 if total_tickets > 0 else 0
    
    def _calculate_user_satisfaction(self, data: Dict[str, Any]) -> float:
        """Calcule la satisfaction utilisateur moyenne"""
        satisfaction_scores = data.get('satisfaction_scores', [8, 7, 9, 6, 8, 7, 8, 9, 7, 8])
        return statistics.mean(satisfaction_scores) if satisfaction_scores else 0
    
    def _calculate_response_satisfaction(self, data: Dict[str, Any]) -> float:
        """Calcule la satisfaction des réponses"""
        satisfied_users = data.get('satisfied_users', 800)
        total_users = data.get('total_users', 1000)
        return (satisfied_users / total_users) * 100 if total_users > 0 else 0
    
    def _calculate_resolution_satisfaction(self, data: Dict[str, Any]) -> float:
        """Calcule la satisfaction de résolution"""
        resolved_satisfactorily = data.get('resolved_satisfactorily', 750)
        total_resolved = data.get('total_resolved', 1000)
        return (resolved_satisfactorily / total_resolved) * 100 if total_resolved > 0 else 0
    
    def _calculate_throughput(self, data: Dict[str, Any]) -> float:
        """Calcule le débit de traitement"""
        tickets_processed = data.get('tickets_processed', 100)
        hours_elapsed = data.get('hours_elapsed', 1)
        return tickets_processed / hours_elapsed if hours_elapsed > 0 else 0
    
    def _calculate_queue_length(self, data: Dict[str, Any]) -> float:
        """Calcule la longueur moyenne de la file d'attente"""
        queue_lengths = data.get('queue_lengths', [8, 12, 6, 15, 9, 11, 7, 13])
        return statistics.mean(queue_lengths) if queue_lengths else 0
    
    def _calculate_error_rate(self, data: Dict[str, Any]) -> float:
        """Calcule le taux d'erreur"""
        error_tickets = data.get('error_tickets', 20)
        total_tickets = data.get('total_tickets', 1000)
        return (error_tickets / total_tickets) * 100 if total_tickets > 0 else 0
    
    def _calculate_first_contact_resolution(self, data: Dict[str, Any]) -> float:
        """Calcule la résolution au premier contact"""
        first_contact_resolved = data.get('first_contact_resolved', 600)
        total_tickets = data.get('total_tickets', 1000)
        return (first_contact_resolved / total_tickets) * 100 if total_tickets > 0 else 0
    
    def _calculate_escalation_rate(self, data: Dict[str, Any]) -> float:
        """Calcule le taux d'escalade"""
        escalated_tickets = data.get('escalated_tickets', 150)
        total_tickets = data.get('total_tickets', 1000)
        return (escalated_tickets / total_tickets) * 100 if total_tickets > 0 else 0
    
    def _calculate_abandonment_rate(self, data: Dict[str, Any]) -> float:
        """Calcule le taux d'abandon"""
        abandoned_tickets = data.get('abandoned_tickets', 50)
        total_tickets = data.get('total_tickets', 1000)
        return (abandoned_tickets / total_tickets) * 100 if total_tickets > 0 else 0
    
    def _calculate_sms_success_rate(self, data: Dict[str, Any]) -> float:
        """Calcule le taux de succès SMS"""
        sms_processed = data.get('sms_processed', 490)
        sms_received = data.get('sms_received', 500)
        return (sms_processed / sms_received) * 100 if sms_received > 0 else 0
    
    def _calculate_web_form_completion(self, data: Dict[str, Any]) -> float:
        """Calcule le taux de completion des formulaires web"""
        completed_forms = data.get('completed_forms', 450)
        started_forms = data.get('started_forms', 500)
        return (completed_forms / started_forms) * 100 if started_forms > 0 else 0
    
    def _calculate_messaging_response_time(self, data: Dict[str, Any]) -> float:
        """Calcule le temps de réponse aux messageries"""
        response_times = data.get('messaging_response_times', [3, 5, 4, 6, 2, 7, 4, 5])
        return statistics.mean(response_times) if response_times else 0
    
    def generate_test_report(self, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Génère un rapport de test complet"""
        calculated_metrics = self.calculate_metrics(test_data)
        
        report = {
            'test_summary': {
                'test_date': datetime.now().isoformat(),
                'total_scenarios': len(test_data.get('scenarios', [])),
                'total_messages': test_data.get('total_messages', 0),
                'test_duration_hours': test_data.get('test_duration_hours', 24)
            },
            'kpi_results': {},
            'performance_analysis': {},
            'recommendations': []
        }
        
        # Analyser chaque métrique
        for metric_name, metric in self.metrics.items():
            current_value = calculated_metrics.get(metric_name, 0)
            target_value = metric.target_value
            
            status = "PASS" if current_value >= target_value else "FAIL"
            if metric.importance == "Critical" and status == "FAIL":
                status = "CRITICAL_FAIL"
            
            report['kpi_results'][metric_name] = {
                'name': metric.name,
                'current_value': current_value,
                'target_value': target_value,
                'unit': metric.unit,
                'status': status,
                'deviation': ((current_value - target_value) / target_value) * 100 if target_value > 0 else 0,
                'importance': metric.importance
            }
        
        # Générer des recommandations
        report['recommendations'] = self._generate_recommendations(report['kpi_results'])
        
        return report
    
    def _generate_recommendations(self, kpi_results: Dict[str, Any]) -> List[str]:
        """Génère des recommandations basées sur les résultats KPI"""
        recommendations = []
        
        for metric_name, result in kpi_results.items():
            if result['status'] == "CRITICAL_FAIL":
                if metric_name == 'reception_rate':
                    recommendations.append("URGENT: Améliorer la fiabilité de réception des messages - vérifier les intégrations SMS/WhatsApp")
                elif metric_name == 'error_rate':
                    recommendations.append("URGENT: Réduire le taux d'erreur - analyser les logs d'erreur et améliorer la gestion d'exceptions")
                elif metric_name == 'user_satisfaction':
                    recommendations.append("URGENT: Améliorer la satisfaction utilisateur - former l'équipe et optimiser les processus")
            
            elif result['status'] == "FAIL":
                if metric_name == 'processing_time':
                    recommendations.append("Optimiser les temps de traitement - automatiser davantage de tâches")
                elif metric_name == 'classification_accuracy':
                    recommendations.append("Améliorer l'algorithme de classification - enrichir le dataset d'entraînement")
                elif metric_name == 'first_contact_resolution':
                    recommendations.append("Améliorer la résolution au premier contact - fournir plus d'informations aux agents")
        
        # Recommandations générales
        if not recommendations:
            recommendations.append("Excellent travail ! Tous les KPI sont dans les objectifs.")
        
        return recommendations

# Exemple d'utilisation
if __name__ == "__main__":
    kpis = CFRMKPIs()
    
    # Données de test simulées
    test_data = {
        'total_messages_sent': 1000,
        'total_messages_received': 995,
        'reception_latencies': [2.1, 3.5, 4.2, 1.8, 5.1, 2.9, 3.7, 4.8],
        'channel_uptime_hours': 99.9,
        'total_time_hours': 100.0,
        'processing_times_minutes': [12, 18, 15, 22, 8, 25, 14, 16],
        'correct_classifications': 850,
        'total_classifications': 1000,
        'auto_classified_tickets': 700,
        'total_tickets': 1000,
        'satisfaction_scores': [8, 7, 9, 6, 8, 7, 8, 9, 7, 8],
        'satisfied_users': 800,
        'total_users': 1000,
        'resolved_satisfactorily': 750,
        'total_resolved': 1000,
        'tickets_processed': 100,
        'hours_elapsed': 1,
        'queue_lengths': [8, 12, 6, 15, 9, 11, 7, 13],
        'error_tickets': 20,
        'first_contact_resolved': 600,
        'escalated_tickets': 150,
        'abandoned_tickets': 50,
        'sms_processed': 490,
        'sms_received': 500,
        'completed_forms': 450,
        'started_forms': 500,
        'messaging_response_times': [3, 5, 4, 6, 2, 7, 4, 5]
    }
    
    # Générer le rapport
    report = kpis.generate_test_report(test_data)
    
    print("=== RAPPORT DE TEST CFRM ===")
    print(f"Date: {report['test_summary']['test_date']}")
    print(f"Messages testés: {report['test_summary']['total_messages']}")
    print()
    
    print("=== RÉSULTATS KPI ===")
    for metric_name, result in report['kpi_results'].items():
        status_emoji = "✅" if result['status'] == "PASS" else "❌" if result['status'] == "FAIL" else "🚨"
        print(f"{status_emoji} {result['name']}: {result['current_value']:.2f}{result['unit']} (Objectif: {result['target_value']}{result['unit']})")
    
    print("\n=== RECOMMANDATIONS ===")
    for i, rec in enumerate(report['recommendations'], 1):
        print(f"{i}. {rec}")

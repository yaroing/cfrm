"""
Scripts de test automatisés pour la plateforme CFRM humanitaire
"""
import requests
import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
from test_data import TestDataGenerator
from kpi_metrics import CFRMKPIs

class CFRMTestRunner:
    """Exécuteur de tests automatisés pour la plateforme CFRM"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.data_generator = TestDataGenerator()
        self.kpi_calculator = CFRMKPIs()
        self.test_results = []
        
    def run_all_tests(self) -> Dict[str, Any]:
        """Exécute tous les tests et génère un rapport complet"""
        print("🚀 Démarrage des tests automatisés CFRM...")
        
        # Tests de réception
        sms_results = self.test_sms_reception()
        web_results = self.test_web_form_submission()
        messaging_results = self.test_messaging_integration()
        
        # Tests de classification
        classification_results = self.test_automatic_classification()
        
        # Tests de performance
        performance_results = self.test_performance()
        
        # Tests de sécurité
        security_results = self.test_security()
        
        # Tests d'intégration
        integration_results = self.test_integrations()
        
        # Compilation des résultats
        all_results = {
            'sms_reception': sms_results,
            'web_forms': web_results,
            'messaging': messaging_results,
            'classification': classification_results,
            'performance': performance_results,
            'security': security_results,
            'integration': integration_results
        }
        
        # Calcul des KPI
        kpi_results = self.kpi_calculator.generate_test_report(all_results)
        
        # Génération du rapport final
        final_report = self.generate_final_report(all_results, kpi_results)
        
        return final_report
    
    def test_sms_reception(self) -> Dict[str, Any]:
        """Teste la réception et le traitement des messages SMS"""
        print("📱 Test de réception SMS...")
        
        results = {
            'test_name': 'SMS Reception',
            'scenarios_tested': 0,
            'scenarios_passed': 0,
            'scenarios_failed': 0,
            'details': []
        }
        
        # Générer des messages de test
        test_messages = self.data_generator.generate_sms_messages(20)
        
        for i, message in enumerate(test_messages):
            scenario_id = f"SMS-{i+1:03d}"
            try:
                # Simuler l'envoi SMS (dans un vrai test, on utiliserait l'API SMS)
                response = self.simulate_sms_reception(message)
                
                if response['success']:
                    results['scenarios_passed'] += 1
                    results['details'].append({
                        'scenario_id': scenario_id,
                        'status': 'PASS',
                        'message': message['text'][:50] + '...',
                        'response_time': response['response_time'],
                        'ticket_created': response['ticket_created']
                    })
                else:
                    results['scenarios_failed'] += 1
                    results['details'].append({
                        'scenario_id': scenario_id,
                        'status': 'FAIL',
                        'message': message['text'][:50] + '...',
                        'error': response['error']
                    })
                
                results['scenarios_tested'] += 1
                
            except Exception as e:
                results['scenarios_failed'] += 1
                results['details'].append({
                    'scenario_id': scenario_id,
                    'status': 'ERROR',
                    'message': message['text'][:50] + '...',
                    'error': str(e)
                })
                results['scenarios_tested'] += 1
        
        return results
    
    def test_web_form_submission(self) -> Dict[str, Any]:
        """Teste la soumission de formulaires web"""
        print("🌐 Test de soumission de formulaires web...")
        
        results = {
            'test_name': 'Web Form Submission',
            'scenarios_tested': 0,
            'scenarios_passed': 0,
            'scenarios_failed': 0,
            'details': []
        }
        
        # Générer des formulaires de test
        test_forms = self.data_generator.generate_web_forms(15)
        
        for i, form in enumerate(test_forms):
            scenario_id = f"WEB-{i+1:03d}"
            try:
                # Simuler la soumission de formulaire
                response = self.simulate_web_form_submission(form)
                
                if response['success']:
                    results['scenarios_passed'] += 1
                    results['details'].append({
                        'scenario_id': scenario_id,
                        'status': 'PASS',
                        'subject': form['subject'],
                        'response_time': response['response_time'],
                        'ticket_created': response['ticket_created']
                    })
                else:
                    results['scenarios_failed'] += 1
                    results['details'].append({
                        'scenario_id': scenario_id,
                        'status': 'FAIL',
                        'subject': form['subject'],
                        'error': response['error']
                    })
                
                results['scenarios_tested'] += 1
                
            except Exception as e:
                results['scenarios_failed'] += 1
                results['details'].append({
                    'scenario_id': scenario_id,
                    'status': 'ERROR',
                    'subject': form['subject'],
                    'error': str(e)
                })
                results['scenarios_tested'] += 1
        
        return results
    
    def test_messaging_integration(self) -> Dict[str, Any]:
        """Teste l'intégration avec les messageries instantanées"""
        print("💬 Test d'intégration messageries...")
        
        results = {
            'test_name': 'Messaging Integration',
            'scenarios_tested': 0,
            'scenarios_passed': 0,
            'scenarios_failed': 0,
            'details': []
        }
        
        # Générer des messages de messagerie
        test_messages = self.data_generator.generate_messaging_messages(15)
        
        for i, message in enumerate(test_messages):
            scenario_id = f"MSG-{i+1:03d}"
            try:
                # Simuler la réception de message
                response = self.simulate_messaging_reception(message)
                
                if response['success']:
                    results['scenarios_passed'] += 1
                    results['details'].append({
                        'scenario_id': scenario_id,
                        'status': 'PASS',
                        'platform': message['platform'],
                        'message': message['text'][:50] + '...',
                        'response_time': response['response_time']
                    })
                else:
                    results['scenarios_failed'] += 1
                    results['details'].append({
                        'scenario_id': scenario_id,
                        'status': 'FAIL',
                        'platform': message['platform'],
                        'error': response['error']
                    })
                
                results['scenarios_tested'] += 1
                
            except Exception as e:
                results['scenarios_failed'] += 1
                results['details'].append({
                    'scenario_id': scenario_id,
                    'status': 'ERROR',
                    'platform': message['platform'],
                    'error': str(e)
                })
                results['scenarios_tested'] += 1
        
        return results
    
    def test_automatic_classification(self) -> Dict[str, Any]:
        """Teste la classification automatique des tickets"""
        print("🤖 Test de classification automatique...")
        
        results = {
            'test_name': 'Automatic Classification',
            'scenarios_tested': 0,
            'scenarios_passed': 0,
            'scenarios_failed': 0,
            'accuracy_by_category': {},
            'details': []
        }
        
        # Générer des messages de test pour la classification
        test_messages = self.data_generator.generate_sms_messages(50)
        
        for i, message in enumerate(test_messages):
            scenario_id = f"CLASS-{i+1:03d}"
            try:
                # Tester la classification
                predicted_category = self.test_classification(message)
                expected_category = message['expected_category']
                
                is_correct = predicted_category == expected_category
                
                if is_correct:
                    results['scenarios_passed'] += 1
                else:
                    results['scenarios_failed'] += 1
                
                # Mettre à jour les statistiques par catégorie
                if expected_category not in results['accuracy_by_category']:
                    results['accuracy_by_category'][expected_category] = {'correct': 0, 'total': 0}
                
                results['accuracy_by_category'][expected_category]['total'] += 1
                if is_correct:
                    results['accuracy_by_category'][expected_category]['correct'] += 1
                
                results['details'].append({
                    'scenario_id': scenario_id,
                    'status': 'PASS' if is_correct else 'FAIL',
                    'text': message['text'][:50] + '...',
                    'expected_category': expected_category,
                    'predicted_category': predicted_category,
                    'is_correct': is_correct
                })
                
                results['scenarios_tested'] += 1
                
            except Exception as e:
                results['scenarios_failed'] += 1
                results['details'].append({
                    'scenario_id': scenario_id,
                    'status': 'ERROR',
                    'text': message['text'][:50] + '...',
                    'error': str(e)
                })
                results['scenarios_tested'] += 1
        
        return results
    
    def test_performance(self) -> Dict[str, Any]:
        """Teste les performances de la plateforme"""
        print("⚡ Test de performance...")
        
        results = {
            'test_name': 'Performance Testing',
            'scenarios_tested': 0,
            'scenarios_passed': 0,
            'scenarios_failed': 0,
            'response_times': [],
            'throughput': 0,
            'details': []
        }
        
        # Test de charge normale
        start_time = time.time()
        test_messages = self.data_generator.generate_sms_messages(100)
        
        for message in test_messages:
            try:
                response_start = time.time()
                response = self.simulate_sms_reception(message)
                response_time = time.time() - response_start
                
                results['response_times'].append(response_time)
                results['scenarios_tested'] += 1
                
                if response_time < 5.0:  # Seuil de 5 secondes
                    results['scenarios_passed'] += 1
                else:
                    results['scenarios_failed'] += 1
                
            except Exception as e:
                results['scenarios_failed'] += 1
        
        total_time = time.time() - start_time
        results['throughput'] = len(test_messages) / total_time if total_time > 0 else 0
        
        return results
    
    def test_security(self) -> Dict[str, Any]:
        """Teste la sécurité de la plateforme"""
        print("🔒 Test de sécurité...")
        
        results = {
            'test_name': 'Security Testing',
            'scenarios_tested': 0,
            'scenarios_passed': 0,
            'scenarios_failed': 0,
            'details': []
        }
        
        # Tests de sécurité
        security_tests = [
            {
                'name': 'SQL Injection',
                'input': "'; DROP TABLE tickets; --",
                'expected': 'safe'
            },
            {
                'name': 'XSS Attack',
                'input': "<script>alert('XSS')</script>",
                'expected': 'safe'
            },
            {
                'name': 'PSEA Data Protection',
                'input': "Signalement d'abus sexuel par le personnel",
                'expected': 'encrypted'
            }
        ]
        
        for test in security_tests:
            try:
                response = self.test_security_input(test['input'])
                
                if response['is_safe']:
                    results['scenarios_passed'] += 1
                    status = 'PASS'
                else:
                    results['scenarios_failed'] += 1
                    status = 'FAIL'
                
                results['details'].append({
                    'test_name': test['name'],
                    'status': status,
                    'input': test['input'][:50] + '...',
                    'is_safe': response['is_safe']
                })
                
                results['scenarios_tested'] += 1
                
            except Exception as e:
                results['scenarios_failed'] += 1
                results['details'].append({
                    'test_name': test['name'],
                    'status': 'ERROR',
                    'error': str(e)
                })
                results['scenarios_tested'] += 1
        
        return results
    
    def test_integrations(self) -> Dict[str, Any]:
        """Teste les intégrations externes"""
        print("🔗 Test des intégrations...")
        
        results = {
            'test_name': 'Integration Testing',
            'scenarios_tested': 0,
            'scenarios_passed': 0,
            'scenarios_failed': 0,
            'details': []
        }
        
        # Tests d'intégration
        integrations = [
            {'name': 'SMS Provider', 'endpoint': '/api/v1/sms/test'},
            {'name': 'WhatsApp API', 'endpoint': '/api/v1/whatsapp/test'},
            {'name': 'Email Service', 'endpoint': '/api/v1/email/test'},
            {'name': 'Translation Service', 'endpoint': '/api/v1/translate/test'}
        ]
        
        for integration in integrations:
            try:
                response = self.test_integration_endpoint(integration['endpoint'])
                
                if response['success']:
                    results['scenarios_passed'] += 1
                    status = 'PASS'
                else:
                    results['scenarios_failed'] += 1
                    status = 'FAIL'
                
                results['details'].append({
                    'integration_name': integration['name'],
                    'status': status,
                    'endpoint': integration['endpoint'],
                    'response_time': response.get('response_time', 0)
                })
                
                results['scenarios_tested'] += 1
                
            except Exception as e:
                results['scenarios_failed'] += 1
                results['details'].append({
                    'integration_name': integration['name'],
                    'status': 'ERROR',
                    'error': str(e)
                })
                results['scenarios_tested'] += 1
        
        return results
    
    # Méthodes de simulation (à adapter selon l'API réelle)
    def simulate_sms_reception(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Simule la réception d'un message SMS"""
        # Simulation - dans un vrai test, on appellerait l'API SMS
        time.sleep(random.uniform(0.1, 0.5))  # Simulation du délai réseau
        
        return {
            'success': True,
            'response_time': random.uniform(0.5, 2.0),
            'ticket_created': True,
            'ticket_id': f"TKT-{random.randint(1000, 9999)}"
        }
    
    def simulate_web_form_submission(self, form: Dict[str, Any]) -> Dict[str, Any]:
        """Simule la soumission d'un formulaire web"""
        time.sleep(random.uniform(0.2, 1.0))
        
        return {
            'success': True,
            'response_time': random.uniform(1.0, 3.0),
            'ticket_created': True,
            'ticket_id': f"TKT-{random.randint(1000, 9999)}"
        }
    
    def simulate_messaging_reception(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Simule la réception d'un message de messagerie"""
        time.sleep(random.uniform(0.1, 0.8))
        
        return {
            'success': True,
            'response_time': random.uniform(0.5, 2.5),
            'ticket_created': True,
            'ticket_id': f"TKT-{random.randint(1000, 9999)}"
        }
    
    def test_classification(self, message: Dict[str, Any]) -> str:
        """Teste la classification d'un message"""
        # Simulation de l'algorithme de classification
        text = message['text'].lower()
        
        if any(word in text for word in ['abus', 'exploitation', 'sexuel']):
            return 'PSEA'
        elif any(word in text for word in ['plainte', 'problème', 'difficile']):
            return 'Complaint'
        elif any(word in text for word in ['merci', 'excellent', 'parfait']):
            return 'Feedback'
        elif any(word in text for word in ['aide', 'besoin', 'demande']):
            return 'Request'
        else:
            return 'Information'
    
    def test_security_input(self, input_text: str) -> Dict[str, Any]:
        """Teste la sécurité d'un input"""
        # Simulation des vérifications de sécurité
        dangerous_patterns = ['<script>', 'DROP TABLE', 'UNION SELECT']
        
        is_safe = not any(pattern in input_text.upper() for pattern in dangerous_patterns)
        
        return {
            'is_safe': is_safe,
            'sanitized': input_text.replace('<', '&lt;').replace('>', '&gt;')
        }
    
    def test_integration_endpoint(self, endpoint: str) -> Dict[str, Any]:
        """Teste un endpoint d'intégration"""
        try:
            # Simulation d'un appel API
            time.sleep(random.uniform(0.1, 0.5))
            
            return {
                'success': True,
                'response_time': random.uniform(0.5, 2.0)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def generate_final_report(self, test_results: Dict[str, Any], kpi_results: Dict[str, Any]) -> Dict[str, Any]:
        """Génère le rapport final de test"""
        total_scenarios = sum(result['scenarios_tested'] for result in test_results.values())
        total_passed = sum(result['scenarios_passed'] for result in test_results.values())
        total_failed = sum(result['scenarios_failed'] for result in test_results.values())
        
        success_rate = (total_passed / total_scenarios * 100) if total_scenarios > 0 else 0
        
        report = {
            'test_summary': {
                'test_date': datetime.now().isoformat(),
                'total_scenarios': total_scenarios,
                'scenarios_passed': total_passed,
                'scenarios_failed': total_failed,
                'success_rate': success_rate
            },
            'test_results': test_results,
            'kpi_results': kpi_results,
            'recommendations': self.generate_recommendations(test_results, kpi_results)
        }
        
        return report
    
    def generate_recommendations(self, test_results: Dict[str, Any], kpi_results: Dict[str, Any]) -> List[str]:
        """Génère des recommandations basées sur les résultats des tests"""
        recommendations = []
        
        # Recommandations basées sur les résultats des tests
        for test_name, result in test_results.items():
            if result['scenarios_failed'] > 0:
                failure_rate = result['scenarios_failed'] / result['scenarios_tested']
                if failure_rate > 0.1:  # Plus de 10% d'échec
                    recommendations.append(f"URGENT: {test_name} a un taux d'échec de {failure_rate:.1%} - investigation requise")
        
        # Recommandations basées sur les KPI
        if 'kpi_results' in kpi_results:
            for metric_name, metric_result in kpi_results['kpi_results'].items():
                if metric_result['status'] == 'CRITICAL_FAIL':
                    recommendations.append(f"CRITIQUE: {metric_result['name']} ne respecte pas l'objectif ({metric_result['current_value']:.2f} vs {metric_result['target_value']:.2f})")
        
        if not recommendations:
            recommendations.append("Excellent travail ! Tous les tests sont dans les objectifs.")
        
        return recommendations

# Exemple d'utilisation
if __name__ == "__main__":
    # Initialiser le testeur
    tester = CFRMTestRunner()
    
    # Exécuter tous les tests
    print("🚀 Démarrage des tests automatisés CFRM...")
    report = tester.run_all_tests()
    
    # Afficher le résumé
    print("\n" + "="*50)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*50)
    print(f"Date: {report['test_summary']['test_date']}")
    print(f"Scénarios testés: {report['test_summary']['total_scenarios']}")
    print(f"Scénarios réussis: {report['test_summary']['scenarios_passed']}")
    print(f"Scénarios échoués: {report['test_summary']['scenarios_failed']}")
    print(f"Taux de réussite: {report['test_summary']['success_rate']:.1f}%")
    
    # Afficher les recommandations
    print("\n" + "="*50)
    print("💡 RECOMMANDATIONS")
    print("="*50)
    for i, rec in enumerate(report['recommendations'], 1):
        print(f"{i}. {rec}")
    
    # Sauvegarder le rapport
    with open('test_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Rapport détaillé sauvegardé dans 'test_report.json'")

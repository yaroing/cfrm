#!/usr/bin/env python3
"""
Script d'exécution des tests pour la plateforme CFRM humanitaire
"""
import sys
import os
import json
from datetime import datetime

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.test_automation import CFRMTestRunner
from tests.test_data import TestDataGenerator
from tests.kpi_metrics import CFRMKPIs

def main():
    """Fonction principale d'exécution des tests"""
    print("🚀 Plateforme CFRM - Tests Automatisés")
    print("=" * 50)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Contexte: Feedback Communautaire Humanitaire")
    print("=" * 50)
    
    # Configuration
    base_url = "http://localhost:8000"
    
    try:
        # Initialiser le testeur
        print("\n🔧 Initialisation du système de test...")
        tester = CFRMTestRunner(base_url)
        
        # Générer des données de test
        print("📊 Génération des données de test...")
        data_generator = TestDataGenerator()
        
        # Afficher un échantillon des données générées
        sms_sample = data_generator.generate_sms_messages(5)
        web_sample = data_generator.generate_web_forms(3)
        msg_sample = data_generator.generate_messaging_messages(3)
        
        print(f"   ✅ {len(sms_sample)} messages SMS générés")
        print(f"   ✅ {len(web_sample)} formulaires web générés")
        print(f"   ✅ {len(msg_sample)} messages de messagerie générés")
        
        # Exécuter les tests
        print("\n🧪 Exécution des tests...")
        report = tester.run_all_tests()
        
        # Afficher le résumé
        print("\n" + "=" * 50)
        print("📊 RÉSUMÉ DES TESTS")
        print("=" * 50)
        
        summary = report['test_summary']
        print(f"📅 Date: {summary['test_date']}")
        print(f"🎯 Scénarios testés: {summary['total_scenarios']}")
        print(f"✅ Scénarios réussis: {summary['scenarios_passed']}")
        print(f"❌ Scénarios échoués: {summary['scenarios_failed']}")
        print(f"📈 Taux de réussite: {summary['success_rate']:.1f}%")
        
        # Afficher les résultats par type de test
        print("\n📋 DÉTAIL PAR TYPE DE TEST")
        print("-" * 30)
        
        for test_name, result in report['test_results'].items():
            if isinstance(result, dict) and 'test_name' in result:
                success_rate = (result['scenarios_passed'] / result['scenarios_tested'] * 100) if result['scenarios_tested'] > 0 else 0
                status_emoji = "✅" if success_rate >= 90 else "⚠️" if success_rate >= 70 else "❌"
                print(f"{status_emoji} {result['test_name']}: {success_rate:.1f}% ({result['scenarios_passed']}/{result['scenarios_tested']})")
        
        # Afficher les KPI
        if 'kpi_results' in report and report['kpi_results']:
            print("\n📊 INDICATEURS DE PERFORMANCE")
            print("-" * 30)
            
            for metric_name, metric_result in report['kpi_results'].items():
                if isinstance(metric_result, dict) and 'name' in metric_result:
                    status_emoji = "✅" if metric_result['status'] == 'PASS' else "⚠️" if metric_result['status'] == 'FAIL' else "🚨"
                    print(f"{status_emoji} {metric_result['name']}: {metric_result['current_value']:.2f}{metric_result['unit']} (Objectif: {metric_result['target_value']}{metric_result['unit']})")
        
        # Afficher les recommandations
        if 'recommendations' in report and report['recommendations']:
            print("\n💡 RECOMMANDATIONS")
            print("-" * 30)
            for i, rec in enumerate(report['recommendations'], 1):
                print(f"{i}. {rec}")
        
        # Sauvegarder le rapport
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_filename = f"test_report_{timestamp}.json"
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Rapport détaillé sauvegardé: {report_filename}")
        
        # Déterminer le code de sortie
        if summary['success_rate'] >= 90:
            print("\n🎉 Tests terminés avec succès !")
            return 0
        elif summary['success_rate'] >= 70:
            print("\n⚠️ Tests terminés avec des avertissements.")
            return 1
        else:
            print("\n❌ Tests échoués - action requise.")
            return 2
            
    except Exception as e:
        print(f"\n💥 Erreur lors de l'exécution des tests: {str(e)}")
        return 3

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

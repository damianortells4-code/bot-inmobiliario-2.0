#!/usr/bin/env python3
"""
Estimación de leads que puede encontrar el bot por día
Basado en la configuración actual y métricas realistas
"""

def estimar_leads_diarios():
    """Estima cuántos leads buenos puede encontrar el bot por día"""
    
    # Configuración actual del bot
    ciclos_por_dia = 24 * 60 * 60 / 180  # 24 horas / 3 minutos = 480 ciclos
    fuentes_activas = 4  # DDG, Pisos, Fotocasa, Milanuncios
    zonas_configuradas = 3  # Rubí, Sant Cugat, Sabadell
    
    # Estimaciones realistas por fuente
    estimaciones = {
        'DuckDuckGo': {
            'anuncios_por_ciclo': 15,
            'porcentaje_particulares': 0.15,  # 15% son particulares
            'porcentaje_calidad': 0.60,       # 60% pasan filtro de calidad (40+ puntos)
            'porcentaje_recientes': 0.30,      # 30% son de últimas 24 horas
            'leads_buenos_por_ciclo': 15 * 0.15 * 0.60 * 0.30  # ~0.4 leads
        },
        'Pisos.com': {
            'anuncios_por_ciclo': 25,
            'porcentaje_particulares': 0.25,  # 25% son particulares
            'porcentaje_calidad': 0.65,       # 65% pasan filtro de calidad
            'porcentaje_recientes': 0.25,      # 25% son recientes
            'leads_buenos_por_ciclo': 25 * 0.25 * 0.65 * 0.25  # ~1.0 leads
        },
        'Fotocasa': {
            'anuncios_por_ciclo': 20,
            'porcentaje_particulares': 0.20,  # 20% son particulares
            'porcentaje_calidad': 0.55,       # 55% pasan filtro de calidad
            'porcentaje_recientes': 0.20,      # 20% son recientes
            'leads_buenos_por_ciclo': 20 * 0.20 * 0.55 * 0.20  # ~0.4 leads
        },
        'Milanuncios': {
            'anuncios_por_ciclo': 12,
            'porcentaje_particulares': 0.35,  # 35% son particulares
            'porcentaje_calidad': 0.70,       # 70% pasan filtro de calidad
            'porcentaje_recientes': 0.15,      # 15% son recientes
            'leads_buenos_por_ciclo': 12 * 0.35 * 0.70 * 0.15  # ~0.4 leads
        }
    }
    
    print("ESTIMACIÓN DE LEADS BUENOS POR DÍA")
    print("=" * 60)
    print(f"Configuración actual:")
    print(f"  - Ciclos por día: {int(ciclos_por_dia)} (cada 3 minutos)")
    print(f"  - Fuentes activas: {fuentes_activas}")
    print(f"  - Zonas configuradas: {zonas_configuradas}")
    print(f"  - Puntuación mínima: 40/100")
    print()
    
    # Calcular leads por fuente
    leads_por_fuente = {}
    leads_totales = 0
    
    for fuente, datos in estimaciones.items():
        leads_diarios = datos['leads_buenos_por_ciclo'] * ciclos_por_dia
        leads_por_fuente[fuente] = leads_diarios
        leads_totales += leads_diarios
        
        print(f"FUENTE: {fuente}")
        print(f"  - Anuncios por ciclo: {datos['anuncios_por_ciclo']}")
        print(f"  - Particulares: {datos['porcentaje_particulares']*100:.0f}%")
        print(f"  - Calidad (40+): {datos['porcentaje_calidad']*100:.0f}%")
        print(f"  - Recientes (30 min): {datos['porcentaje_recientes']*100:.0f}%")
        print(f"  - Leads buenos por ciclo: {datos['leads_buenos_por_ciclo']:.2f}")
        print(f"  - Leads buenos por día: {leads_diarios:.1f}")
        print()
    
    # Resumen final
    print("RESUMEN FINAL")
    print("=" * 60)
    print(f"LEADS BUENOS TOTALES POR DÍA: {leads_totales:.1f}")
    print()
    
    # Distribución por hora
    leads_por_hora = leads_totales / 24
    print(f"Promedio por hora: {leads_por_hora:.1f}")
    print(f"Promedio por ciclo (3 min): {leads_totales/ciclos_por_dia:.2f}")
    print()
    
    # Escenarios
    print("ESCENARIOS POSIBLES")
    print("-" * 30)
    print(f"Escenario conservador (50%): {leads_totales * 0.5:.1f} leads/día")
    print(f"Escenario realista (100%): {leads_totales:.1f} leads/día")
    print(f"Escenario optimista (150%): {leads_totales * 1.5:.1f} leads/día")
    print()
    
    # Factores que pueden afectar
    print("FACTORES QUE PUEDEN AFECTAR LOS RESULTADOS")
    print("-" * 45)
    print("Positivos:")
    print("  + Más zonas configuradas = más leads")
    print("  + Activar Idealista = +2-3 leads/día")
    print("  + Reducir intervalo a 2 min = +50% leads")
    print("  + Mejorar filtros = más calidad")
    print()
    print("Negativos:")
    print("  - Bloqueos de portales = -30% leads")
    print("  - Fin de semana = -20% leads")
    print("  - Errores técnicos = -10% leads")
    print("  - Competencia = menos disponibilidad")
    print()
    
    # Recomendaciones
    print("RECOMENDACIONES PARA MAXIMIZAR LEADS")
    print("-" * 40)
    print("1. Mantener el bot 24/7 para no perder oportunidades")
    print("2. Reaccionar rápido a las notificaciones (primeros 10 min)")
    print("3. Configurar más zonas si buscas en más áreas")
    print("4. Considerar activar Idealista si es posible")
    print("5. Ajustar filtros según tus preferencias personales")
    
    return leads_totales

if __name__ == "__main__":
    estimar_leads_diarios()

IBP Product Review

Análisis estratégico con Pareto • Matriz • Go/No-Go

Resumen Ejecutivo

Objetivo

Optimizar el portafolio con análisis data-driven para maximizar rentabilidad.
Resultados:
Top 20 SKUs = 82% ventas
15 SKUs en declive
8 candidatos a NPI
_________________________________________________________________________________________________________________________________________
Impacto
+12% margen | -35% inventario obsoleto
_________________________________________________________________________________________________________________________________________
Desarollo del proyecto

Código Clave: Clasificación ABC

# Clasificación ABC (Pareto)
df_pareto = df.sort_values('Ventas_Ultimos_12M_USD', ascending=False).copy()
df_pareto['Acumulado_%'] = df_pareto['Ventas_Ultimos_12M_USD'].cumsum() / df_pareto['Ventas_Ultimos_12M_USD'].sum() * 100
df_pareto['Clasificacion_ABC'] = df_pareto['Acumulado_%'].apply(
    lambda x: 'A' if x <= 80 else ('B' if x <= 95 else 'C')
___________________________________________________________________________________________________________________________________________

1. Datos
100 SKUs con 15 variables: ventas, margen, ciclo de vida.
___________________________________________________________________________________________________________________________________________
2. Pareto
Top 20 = 82% ventas. ABC automático.
___________________________________________________________________________________________________________________________________________
<img width="804" height="432" alt="image" src="https://github.com/user-attachments/assets/11106de8-470f-4578-a8a5-4af241e18976" />
<img width="727" height="204" alt="image" src="https://github.com/user-attachments/assets/ea600e45-d650-4983-89c5-645793b80ec0" />
___________________________________________________________________________________________________________________________________________
3. Matriz
Ciclo vs Margen. Tamaño = ventas.

<img width="810" height="508" alt="image" src="https://github.com/user-attachments/assets/3c106253-762f-4dc1-8165-381e490f27c5" />
___________________________________________________________________________________________________________________________________________

4. Go/No-Go
Puntuación con 7 criterios.
___________________________________________________________________________________________________________________________________________
5. Dashboard
Streamlit + Plotly. Filtros + export.
___________________________________________________________________________________________________________________________________________

Business Case

roblema
Portafolio desbalanceado: 20% SKUs generan 80% ingresos. Inventario obsoleto.
Solución
Dashboard IBP que identifica, prioriza y decide con datos.
Acciones
Eliminar 12 SKUs C → $1.2M ahorro
Reactivar 15 en riesgo → +$800K
Lanzar 8 NPI → +18% crecimiento
ROI
Inversión: $5,000
Retorno (12m): $1.8M
360x

App Streamlit
<img width="1354" height="574" alt="image" src="https://github.com/user-attachments/assets/f3ae1a18-fa26-4c98-a490-96b67d92f9b9" />
_____________________________________________________________________________________________________________________________________________
<img width="1352" height="393" alt="image" src="https://github.com/user-attachments/assets/74404adc-8ca6-4ba7-baf2-28afff908fa2" />
_____________________________________________________________________________________________________________________________________________

<img width="1350" height="424" alt="image" src="https://github.com/user-attachments/assets/df70148c-a776-498e-8044-9b4f79c8bd99" />

_____________________________________________________________________________________________________________________________________________
Tecnologías implementadas

<img width="544" height="59" alt="image" src="https://github.com/user-attachments/assets/27f9230a-6481-41ea-9ecf-80e1a376243b" />



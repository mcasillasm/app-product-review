import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import io

# === CONFIGURACIÓN ===
st.set_page_config(
    page_title="IBP Product Review",
    page_icon="bar_chart",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
# IBP Product Review Dashboard
### Análisis Estratégico del Portafolio: Pareto • Matriz • Go/No-Go
""")

# === DATASET EMBEBIDO (100 SKUs) ===
@st.cache_data
def load_data():
    data = {
        'SKU': [f'SKU{i:03d}' for i in range(1, 101)],
        'Nombre_Producto': [
            'Wireless Earbuds X1', 'Smartwatch Pro', 'Laptop Ultra 15"', 'Monitor OLED 32"', 'Tablet Lite 10"', 
            'PowerBank 20000mAh', 'SSD 1TB NVMe', 'Teclado Mecánico RGB', 'Mouse Gaming 16000DPI', 'Hub USB-C 7en1',
            *['Producto Genérico ' + str(i) for i in range(11, 101)]
        ],
        'Categoria': np.random.choice(['Electrónica', 'Accesorios', 'Computo', 'Periféricos'], 100),
        'Etapa_Ciclo_Vida': np.random.choice(['Introducción', 'Crecimiento', 'Madurez', 'Declive'], 100, p=[0.15, 0.25, 0.45, 0.15]),
        'Ventas_Ultimos_12M_USD': np.random.lognormal(mean=10, sigma=1.2, size=100).round(0),
        'Ventas_Pronosticadas_12M_USD': np.random.lognormal(mean=10.1, sigma=1.1, size=100).round(0),
        'Margen_Bruto_Pct': np.random.normal(35, 12, 100).clip(10, 60).round(1),
        'Variacion_YoY_Pct': np.random.normal(15, 40, 100).round(1),
        'Proyectos_NPI': np.random.choice(['Lanzado Q1', 'En Desarrollo', 'Ninguno'], 100, p=[0.2, 0.1, 0.7])
    }
    
    df = pd.DataFrame(data)
    df['Fecha_Lanzamiento'] = pd.to_datetime('2023-01-01') + pd.to_timedelta(np.random.randint(0, 1000, 100), unit='d')
    df['Fecha_Fin_Proyectada'] = df['Fecha_Lanzamiento'] + pd.to_timedelta(np.random.randint(730, 1825, 100), unit='d')
    
    # Ajustar ventas para que haya Pareto real
    ventas_ordenadas = np.sort(df['Ventas_Ultimos_12M_USD'])[::-1]
    ventas_ordenadas = np.concatenate([ventas_ordenadas[:20] * 3, ventas_ordenadas[20:] / 3])
    df['Ventas_Ultimos_12M_USD'] = ventas_ordenadas
    
    return df

df = load_data()

# === FILTROS ===
st.sidebar.header("Filtros")
categoria = st.sidebar.multiselect("Categoría", df['Categoria'].unique(), df['Categoria'].unique())
etapa = st.sidebar.multiselect("Etapa", df['Etapa_Ciclo_Vida'].unique(), df['Etapa_Ciclo_Vida'].unique())
margen = st.sidebar.slider("Margen (%)", 0, 60, (20, 50))
variacion = st.sidebar.slider("Variación YoY (%)", -100, 300, (-50, 100))

df_filtered = df[
    (df['Categoria'].isin(categoria)) &
    (df['Etapa_Ciclo_Vida'].isin(etapa)) &
    (df['Margen_Bruto_Pct'].between(margen[0], margen[1])) &
    (df['Variacion_YoY_Pct'].between(variacion[0], variacion[1]))
].copy()

# === KPIs ===
total_ventas = df_filtered['Ventas_Ultimos_12M_USD'].sum()
total_pronostico = df_filtered['Ventas_Pronosticadas_12M_USD'].sum()
crecimiento = ((total_pronostico / total_ventas) - 1) * 100 if total_ventas > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("SKUs", len(df_filtered))
col2.metric("Ventas 12M", f"${total_ventas:,.0f}")
col3.metric("Pronóstico", f"${total_pronostico:,.0f}")
col4.metric("Crecimiento", f"{crecimiento:+.1f}%")

# === 1. PARETO ===
st.markdown("---")
st.subheader("1. Análisis Pareto 80/20")

df_pareto = df_filtered.sort_values('Ventas_Ultimos_12M_USD', ascending=False).copy()
df_pareto['Acumulado_%'] = df_pareto['Ventas_Ultimos_12M_USD'].cumsum() / total_ventas * 100
df_pareto['Clasificacion_ABC'] = df_pareto['Acumulado_%'].apply(lambda x: 'A' if x <= 80 else ('B' if x <= 95 else 'C'))

top_n = 20
df_top = df_pareto.head(top_n)

fig = go.Figure()
fig.add_trace(go.Bar(x=df_top['SKU'], y=df_top['Ventas_Ultimos_12M_USD']/1000, name="Ventas (kUSD)", marker_color='steelblue'))
fig.add_trace(go.Scatter(x=df_top['SKU'], y=df_top['Acumulado_%'], mode='lines+markers', name="Acumulado %", line=dict(color='red'), yaxis="y2"))
fig.update_layout(
    title=f"Top {top_n} SKUs = {df_top['Acumulado_%'].iloc[-1]:.1f}% de ventas",
    yaxis=dict(title="Ventas (miles USD)"),
    yaxis2=dict(title="Acumulado %", overlaying="y", side="right", range=[0, 105]),
    xaxis_tickangle=45
)
st.plotly_chart(fig, use_container_width=True)

# === 2. MATRIZ ===
st.subheader("2. Matriz: Ciclo de Vida vs Margen")

df_matrix = df_filtered.copy()
df_matrix['Clasificacion_ABC'] = df_pareto['Clasificacion_ABC'].iloc[:len(df_matrix)].values  # Alinear

fig_matrix = px.scatter(
    df_matrix, x='Etapa_Ciclo_Vida', y='Margen_Bruto_Pct',
    size='Ventas_Ultimos_12M_USD', color='Clasificacion_ABC',
    hover_data=['SKU', 'Nombre_Producto'],
    color_discrete_map={'A':'#10b981', 'B':'#f59e0b', 'C':'#ef4444'}
)
st.plotly_chart(fig_matrix, use_container_width=True)

# === 3. GO/NO-GO ===
st.subheader("3. Go/No-Go")

def go_no_go(row):
    score = 0
    if row['Etapa_Ciclo_Vida'] in ['Introducción', 'Crecimiento']: score += 3
    if row['Variacion_YoY_Pct'] >= 30: score += 2
    if row['Margen_Bruto_Pct'] >= 40: score += 2
    if 'Lanzado' in str(row['Proyectos_NPI']): score += 1
    if row['Etapa_Ciclo_Vida'] == 'Declive': score -= 3
    if row['Variacion_YoY_Pct'] <= -40: score -= 2
    if row['Margen_Bruto_Pct'] <= 20: score -= 2
    decision = "GO" if score >= 2 else ("WATCH" if score >= 0 else "NO-GO")
    return pd.Series([decision, score])

df_gng = df_filtered.copy()
df_gng[['Decision', 'Score']] = df_gng.apply(go_no_go, axis=1)

resumen = df_gng['Decision'].value_counts()
fig_pie = px.pie(values=resumen.values, names=resumen.index, color_discrete_map={'GO':'green', 'WATCH':'orange', 'NO-GO':'red'})
st.plotly_chart(fig_pie, use_container_width=True)

# === EXPORTAR ===
st.download_button(
    "Descargar Excel",
    data=df_filtered.to_csv(index=False).encode(),
    file_name="IBP_Product_Review.csv",
    mime="text/csv"
)

st.success("Maribel Casillas")
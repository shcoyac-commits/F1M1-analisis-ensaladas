

import streamlit as st
import pandas as pd
import plotly.express as px
import sys
sys.path.insert(0, '.')
from src.kpis import ticket_promedio, share_por_categoria, pareto_80_20, cliente_activos

# ── Cargar datos ──
df = pd.read_parquet('data/processed/Dataset1_anonimizado.parquet')

# ── Título ──
st.set_page_config(layout="wide")

st.title("Dashboard Leonali — Análisis Retail")
st.caption("Fase 1 · Módulo 1 · Periodo: 2013–2022 · ~581K transacciones")

# ── Sección 1: Vista General ──
st.header("📊 Vista General")

    # ── Filtro ──
años = sorted(df['FechaProceso'].dt.year.unique())
# ── Sidebar ──
st.sidebar.header("Filtros")
rango = st.sidebar.slider("Rango de años", min(años), max(años), (2013, 2022))

categorias = st.sidebar.multiselect(
    "Categorías",
    options=sorted(df['Categoria1'].unique()),
    default=sorted(df['Categoria1'].unique())
)

canales = st.sidebar.multiselect(
    "Canales",
    options=sorted(df['Canal1'].unique()),
    default=sorted(df['Canal1'].unique())
)

df = df[(df['FechaProceso'].dt.year >= rango[0]) & 
        (df['FechaProceso'].dt.year <= rango[1]) & 
        (df['Categoria1'].isin(categorias))]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Venta Total", f"${df['Costo_Venta'].sum()/1_000_000:,.1f}M")
col2.metric("Ticket Promedio", f"${ticket_promedio(df):,.0f}")
col3.metric("Clientes Activos", df['IdCliente'].nunique())
col4.metric("SKUs", df['Producto'].nunique())

# ── Tendencia anual ──
df['año'] = df['FechaProceso'].dt.year
ventas_año = df.groupby('año')['Costo_Venta'].sum().reset_index()

fig_tendencia = px.line(
    ventas_año, x='año', y='Costo_Venta',
    title='Tendencia de Venta Anual'
)
st.plotly_chart(fig_tendencia, use_container_width=True)

# ── Sección 2: Productos ──
st.header("📦 Productos — ¿qué vendemos?")

col_izq, col_der = st.columns(2)

with col_izq:
    pareto = pareto_80_20(df)
    fig_pareto = px.line(
        pareto, x=range(1, len(pareto)+1), y='acumulado',
        title='Curva de Pareto'
    )
    fig_pareto.add_hline(y=80, line_dash="dash", line_color="red")
    fig_pareto.add_hline(y=95, line_dash="dash", line_color="orange")
    st.plotly_chart(fig_pareto, use_container_width=True)

with col_der:
    share = share_por_categoria(df)
    fig_share = px.bar(
        share.sort_values('share', ascending=False),
        x='Categoria1', y='share',
        title='Share por Categoría (%)'
    )
    st.plotly_chart(fig_share, use_container_width=True)

    # ── Sección 3: Tiempo ──



st.header("📅 Tiempo — ¿cuándo vendemos?")

df['mes'] = df['FechaProceso'].dt.month

col_t1, col_t2 = st.columns(2)

with col_t1:
    ventas_mes = df[df['año'].between(2013, 2021)].groupby(['año', 'mes'])['Costo_Venta'].sum().reset_index()
    promedio_anual = df[df['año'].between(2013, 2021)].groupby('año')['Costo_Venta'].sum().reset_index()
    promedio_anual['promedio_mes'] = promedio_anual['Costo_Venta'] / 12
    ventas_mes = ventas_mes.merge(promedio_anual[['año', 'promedio_mes']], on='año')
    ventas_mes['indice'] = ventas_mes['Costo_Venta'] / ventas_mes['promedio_mes']
    indice_prom = ventas_mes.groupby('mes')['indice'].mean().reset_index()

    fig_est = px.bar(
        indice_prom, x='mes', y='indice',
        title='Índice de Estacionalidad Mensual'
    )
    fig_est.add_hline(y=1.0, line_dash="dash", line_color="white", opacity=0.5)
    st.plotly_chart(fig_est, use_container_width=True)

with col_t2:
    ventas_cat_año = df.groupby([df['FechaProceso'].dt.year, 'Categoria1'])['Costo_Venta'].sum().reset_index()
    fig_heat = px.density_heatmap(
        ventas_cat_año, x='FechaProceso', y='Categoria1', z='Costo_Venta',
        title='Venta: Categoría × Año', histfunc='sum'
    )
    st.plotly_chart(fig_heat, use_container_width=True)

# ── Sección 4: Clientes ──
st.header("👥 Clientes — ¿a quién vendemos?")

col_c1, col_c2 = st.columns(2)

with col_c1:
    ctes = cliente_activos(df)
    fig_ctes = px.line(
        ctes, x='FechaProceso', y='IdCliente',
        title='Clientes Activos por Año', markers=True
    )
    st.plotly_chart(fig_ctes, use_container_width=True)

with col_c2:
    clientes = df.groupby('IdCliente').agg(
        gasto_total=('Costo_Venta', 'sum'),
        frecuencia=('FechaProceso', 'nunique')
    )
    import numpy as np
    clientes['seg_gasto'] = pd.qcut(clientes['gasto_total'], q=3, labels=['Bajo', 'Medio', 'Alto'])
    clientes['seg_frecuencia'] = pd.qcut(clientes['frecuencia'], q=3, labels=['Bajo', 'Medio', 'Alto'])
    clientes['segmento'] = clientes['seg_gasto'].astype(str) + ' - ' + clientes['seg_frecuencia'].astype(str)
    seg_counts = clientes['segmento'].value_counts().reset_index()

    fig_seg = px.bar(
        seg_counts, x='segmento', y='count', color='segmento',
        title='Clientes por Segmento'
    )
    st.plotly_chart(fig_seg, use_container_width=True)

    st.divider()
st.caption("Dashboard construido con Streamlit + Plotly | Datos anonimizados | Módulo 1 - F1M1")
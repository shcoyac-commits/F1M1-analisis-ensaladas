import streamlit as st
import pandas as pd
import plotly.express as px
import sys
sys.path.insert(0, '.')
from src.kpis import ticket_promedio, pareto_80_20

st.set_page_config(layout="wide")

# ── Cargar datos ──
df = pd.read_parquet('data/processed/farmacias_ventas_det_anonimizado.parquet')
df['venta'] = df['precio_unit'] * df['cantidad']
df['fecha_venta'] = pd.to_datetime(df['fecha_venta'])
df['año'] = df['fecha_venta'].dt.year
df['mes'] = df['fecha_venta'].dt.month

# Filtrar 2016
df = df[df['año'] == 2016]

st.title("Dashboard Farmacias — Análisis Retail")
st.caption(f"Fase 1 · Módulo 1 · Año 2016 · {df.shape[0]:,} transacciones")
st.metric("Venta Total", f"${df['venta'].sum()/1_000_000:,.1f}M")

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import sys
sys.path.insert(0, '.')
from src.kpis import ticket_promedio, pareto_80_20

st.set_page_config(layout="wide")

# ── Cargar datos ──
@st.cache_data
def cargar_datos():
    df = pd.read_parquet('data/processed/farmacias_ventas_det_anonimizado.parquet')
    df['venta'] = df['precio_unit'] * df['cantidad']
    df['fecha_venta'] = pd.to_datetime(df['fecha_venta'])
    df['año'] = df['fecha_venta'].dt.year
    df['mes'] = df['fecha_venta'].dt.month
    df = df[df['año'] == 2016]
    return df

df = cargar_datos()

# ── Sidebar ──
st.sidebar.header("Filtros")
meses = st.sidebar.slider("Rango de meses", 1, 12, (1, 12))
df = df[(df['mes'] >= meses[0]) & (df['mes'] <= meses[1])]

# ── Título ──
st.title("Dashboard Farmacias — Análisis Retail")
st.caption(f"Fase 1 · Módulo 1 · Año 2016 · {df.shape[0]:,} transacciones · 146 sucursales")

# ── Sección 1: Vista General ──
st.header("📊 Vista General")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Venta Total", f"${df['venta'].sum()/1_000_000:,.1f}M")
col2.metric("Ticket Promedio", f"${ticket_promedio(df, col_venta='venta', col_ticket='folio_venta'):,.0f}")
col3.metric("Tickets", f"{df['folio_venta'].nunique():,}")
col4.metric("SKUs", f"{df['SKU'].nunique():,}")

# Tendencia mensual
ventas_mes = df.groupby('mes')['venta'].sum().reset_index()
fig_tend = px.bar(ventas_mes, x='mes', y='venta', title='Venta Mensual 2016')
st.plotly_chart(fig_tend, use_container_width=True)

# ── Sección 2: Productos ──
st.header("📦 Productos — ¿qué vendemos?")
col_izq, col_der = st.columns(2)

with col_izq:
    pareto = pareto_80_20(df, col_venta='venta', col_grupo='SKU')
    fig_pareto = px.line(pareto, x=range(1, len(pareto)+1), y='acumulado', title='Curva de Pareto')
    fig_pareto.add_hline(y=80, line_dash="dash", line_color="red")
    fig_pareto.add_hline(y=95, line_dash="dash", line_color="orange")
    st.plotly_chart(fig_pareto, use_container_width=True)

with col_der:
    n_a = pareto[pareto['es_80']].shape[0]
    n_b = pareto[(pareto['acumulado'] > 80) & (pareto['acumulado'] <= 95)].shape[0]
    n_c = pareto[pareto['acumulado'] > 95].shape[0]
    abc_data = pd.DataFrame({'clase': ['A', 'B', 'C'], 'productos': [n_a, n_b, n_c]})
    fig_abc = px.bar(abc_data, x='clase', y='productos', color='clase', title='Clasificación ABC — SKUs')
    st.plotly_chart(fig_abc, use_container_width=True)

# ── Sección 3: Tiempo ──
st.header("📅 Tiempo — ¿cuándo vendemos?")
col_t1, col_t2 = st.columns(2)

with col_t1:
    dia = df.copy()
    dia['dia_semana'] = dia['fecha_venta'].dt.day_name()
    orden = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    ventas_dia = dia.groupby('dia_semana')['venta'].sum().reset_index()
    fig_dia = px.bar(ventas_dia, x='dia_semana', y='venta', title='Venta por Día de Semana',
                     category_orders={'dia_semana': orden})
    st.plotly_chart(fig_dia, use_container_width=True)

with col_t2:
    tickets_dia = dia.groupby('dia_semana')['folio_venta'].nunique().reset_index()
    fig_tdia = px.bar(tickets_dia, x='dia_semana', y='folio_venta', title='Tickets por Día de Semana',
                      category_orders={'dia_semana': orden})
    st.plotly_chart(fig_tdia, use_container_width=True)

# ── Sección 4: Sucursales ──
st.header("🏪 Sucursales — ¿dónde vendemos?")
ventas_suc = df.groupby('ID_TIENDA')['venta'].sum().reset_index().sort_values('venta', ascending=False).head(20)
fig_suc = px.bar(ventas_suc, x='ID_TIENDA', y='venta', title='Top 20 Sucursales por Venta')
st.plotly_chart(fig_suc, use_container_width=True)

st.divider()
st.caption("Dashboard construido con Streamlit + Plotly | Datos anonimizados | Módulo 1 - Farmacias")
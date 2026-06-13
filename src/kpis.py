"""
Funciones reutilizables de KPIs para análisis retail.
"""
import pandas as pd

def ticket_promedio(df, col_venta='Costo_Venta', col_ticket=None):
    if col_ticket:
        # Si hay columna de ticket: suma por ticket, luego mediana
        return df.groupby(col_ticket)[col_venta].sum().median()
    else:
        # Si cada fila ya es un ticket
        return df[col_venta].median()

def share_por_categoria(df, col_venta='Costo_Venta', col_grupo='Categoria1'):
    total_venta_cat = df.groupby(col_grupo)[col_venta].sum().reset_index()
    total_venta = df[col_venta].sum()
    total_venta_cat['share'] = total_venta_cat[col_venta] / total_venta * 100
    return total_venta_cat

def pareto_80_20(df, col_venta='Costo_Venta', col_grupo='Producto'):
    total_venta_producto = df.groupby(col_grupo)[col_venta].sum().reset_index()
    total_venta_producto = total_venta_producto.sort_values(col_venta, ascending=False)
    total_venta = df[col_venta].sum()
    total_venta_producto ['acumulado']= total_venta_producto[col_venta].cumsum() / total_venta * 100
    total_venta_producto['es_80']= total_venta_producto['acumulado']<= 80
    return total_venta_producto 
    
def cliente_activos(df, col_cliente='IdCliente', col_fecha='FechaProceso'):
    ctes_activos = df.groupby(df[col_fecha].dt.year)[col_cliente].nunique().reset_index() 
    return ctes_activos
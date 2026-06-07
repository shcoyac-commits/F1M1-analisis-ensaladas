# 🧪 Proyecto DS — Plantilla Analítica

> Plantilla profesional para proyectos de Data Science con estructura estandarizada, ambiente reproducible y flujo de trabajo Git integrado.

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 📋 Descripción

Esta es una plantilla base para proyectos de análisis de datos que incluye:

- ✅ Estructura de carpetas estandarizada
- ✅ Gestión de dependencias con `conda` y `pip`
- ✅ Notebooks organizados y documentados
- ✅ Flujo de trabajo Git documentado
- ✅ Configuración de ambiente reproducible

**Objetivo:** Servir como base para los 8 módulos del roadmap de transición a Data Scientist Jr.

## 🗂️ Estructura del proyecto
proyecto-ds-plantilla/
├── data/
│   ├── raw/              # Datos originales (nunca se modifican)
│   ├── processed/        # Datos limpios listos para análisis
│   └── external/         # Datos de fuentes externas
├── notebooks/            # Jupyter notebooks para exploración y análisis
├── src/                  # Scripts Python reutilizables
├── reports/              # Reportes finales (PDF, HTML, gráficas)
├── requirements.txt      # Dependencias pip
├── environment.yml       # Ambiente conda completo
└── README.md            # Este archivo

## 🚀 Instalación

### Requisitos previos
- [Anaconda](https://www.anaconda.com/download) o [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- Git

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/shcoyac-commits/proyecto-ds-plantilla.git
cd proyecto-ds-plantilla
```

### Paso 2: Crear el ambiente

**Opción A: Con conda (recomendado)**
```bash
conda env create -f environment.yml
conda activate analytics
```

**Opción B: Con pip**
```bash
pip install -r requirements.txt
```

### Paso 3: Abrir JupyterLab

```bash
jupyter lab
```

Los notebooks están en la carpeta `notebooks/`.

## 📚 Contenido actual

### Notebooks completados:
- **S2.1** — Refresco de Python esencial: tipos, listas, dicts, comprehensions, funciones
- **S2.2** — Tour por pandas: Series, DataFrame, groupby, merge, pivot
- **S2.3** — NumPy esencial: arrays, broadcasting, vectorización vs loops
- **S2.4** — Flujo de trabajo: Jupyter + VSCode + Conda + Git

### Aprendizajes clave:
- Vectorización con NumPy (62x más rápido que loops en 1M de registros)
- Limpieza de datos con pandas (nulos, duplicados, tipos)
- Gestión de ambientes reproducibles con conda
- Flujo Git profesional para proyectos DS

## 🛠️ Stack tecnológico

| Categoría | Herramientas |
|-----------|-------------|
| **Lenguaje** | Python 3.11 |
| **Data Science** | NumPy 2.4.4, Pandas 3.0.2, SciPy 1.17.1 |
| **Visualización** | Matplotlib 3.10.8, Seaborn 0.13.2 |
| **Machine Learning** | scikit-learn 1.7.1 |
| **Notebooks** | JupyterLab 4.5.6 |
| **Gestión de ambiente** | Conda, pip |
| **Control de versiones** | Git, GitHub |

## 🔄 Flujo de trabajo Git

```bash
# Antes de empezar
git pull

# Durante la sesión
# ... trabajar en notebooks ...

# Al final
git add .
git commit -m "S2.X Descripción del trabajo"
git push
```

Ver `notebooks/S2.4-flujo-trabajo-git.ipynb` para detalles completos.

## 📖 Próximos pasos

Este repo es la base para desarrollar 8 módulos de análisis:
1. **Módulo 1** — Descriptivo + EDA
2. **Módulo 2** — Diagnóstico (cohortes, retención)
3. **Módulo 3** — Segmentación (RFM, clustering)
4. **Módulo 4** — Asociación (market basket)
5. **Módulo 5** — Forecasting (series temporales)
6. **Módulo 6** — Clasificación (churn, propensión)
7. **Módulo 7** — Optimización (pricing, promociones)
8. **Módulo 8** — Causal inference y A/B testing

## 🔐 Cimiento 2 — Anonimización y Diagnóstico de Calidad (v0.2)

### Datasets incluidos

| Dataset | Origen | Filas | Estado |
|---------|--------|-------|--------|
| Leonali (retail) | SoftRes | ~500K | Anonimizado ✅ |
| Farmacias | SoftRes | ~18.3M | Anonimizado ✅ |
| Restaurante | SoftRes | múltiples tablas | Sin PII — sin cambios ✅ |

Los datos originales **no están en el repositorio** (ver `.gitignore`).
Los datos procesados están en `data/processed/`.

### Cómo regenerar los datasets anonimizados

Si tienes acceso a los archivos originales, puedes regenerar los datasets anonimizados así:

**Requisitos:** ambiente `analytics` activado, archivos originales en `C:\Users\Said\Documents\Datasets\SoftRes\`

```bash
conda activate analytics
```

Luego ejecuta los notebooks en orden:
notebooks/S3.2-anonimizacion-leonali.ipynb      # Anonimiza Leonali
notebooks/S3.3-anonimizacion-farmacias.ipynb    # Anonimiza Farmacias

Los archivos resultantes se guardan automáticamente en `data/processed/`.

### Diagnóstico de calidad

Los reportes Sweetviz están en `reports/` (HTML interactivo por dataset).
El reporte consolidado está en `reports/S3.6_Diagnostico_Calidad_Consolidado.docx`.

Para regenerar los reportes de calidad:
notebooks/S3.6-reportes-calidad.ipynb

### Hallazgos principales

- **Leonali:** Dataset limpio. 13–15% ceros en algunas columnas numéricas (posiblemente reales).
- **Farmacias:** `iva_unit` 62% ceros (medicamentos tasa 0% IVA en México — válido). `tipo_transaccion` 86% ceros — revisar.
- **Restaurante:** Columna `comanda` 100% nula (eliminar). `precio` 27% ceros — revisar. 3 columnas sin valor analítico.

## 🧮 Cimiento 3 — Matemáticas aplicadas para DS (v0.3)

### Sesiones completadas

| Sesión | Tema | Notebook |
|--------|------|----------|
| S4.1 | Estadística descriptiva: media, mediana, varianza, IQR | `notebooks/S4.1-estadistica-descriptiva.ipynb` |
| S4.2 | Distribuciones: Normal, Log-normal, Poisson, Exponencial | `notebooks/S4.2-distribuciones-probabilidad.ipynb` |
| S4.3 | Inferencia estadística: CLT, SE, intervalos de confianza | `notebooks/S4.3-inferencia-basica.ipynb` |
| S4.4 | Álgebra lineal: vectores, distancias, RFM, normalización | `notebooks/S4.4-algebra-lineal.ipynb` |
| S4.5 | Correlación: Pearson, Spearman, matriz de correlación | `notebooks/S4.5-correlacion.ipynb` |
| S4.6 | Test de hipótesis: t-test, p-value, Cohen's d | `notebooks/S4.6-tests-hipotesis.ipynb` |

### Dataset utilizado
- **Leonali** (sell-in retail/alimentos) — `data/processed/dataset1_anonimizado.parquet`


## 👤 Autor

**Said Herrera Coyac**
- GitHub: [@shcoyac-commits](https://github.com/shcoyac-commits)
- Proyecto: Transición a Data Scientist Jr (12-18 meses)

## 📝 Licencia

MIT License - ver archivo [LICENSE](LICENSE) para detalles.

---
**Versión:** v0.3 — Cimiento 3 completado (junio 2026) | Cimiento 2: anonimización y diagnóstico | Cimiento 1: estructura base
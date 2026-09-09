import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración inicial de la página de Streamlit
st.set_page_config(
    page_title="NYSE Financial Analytics - EDA App",
    page_icon="📈",
    layout="wide"
)

# Estilo visual de los gráficos
sns.set_theme(style="whitegrid")


# =========================================================
# CLASE POO: DataAnalyzer (Backend de Procesamiento)
# =========================================================
class DataAnalyzer:
    """
    Clase para el procesamiento, limpieza y análisis exploratorio 
    de datos financieros de la New York Stock Exchange (NYSE).
    """
    def __init__(self, df: pd.DataFrame):
        self.df_raw = df.copy()
        self.df = df.copy()
        self._preprocess()

    def _preprocess(self):
        """Limpia y transforma variables al inicializar el objeto."""
        # 1. Eliminar Unnamed: 0 si funciona como índice secundario
        if 'Unnamed: 0' in self.df.columns:
            self.df = self.df.drop(columns=['Unnamed: 0'])

        # 2. Convertir Period Ending a tipo datetime
        if 'Period Ending' in self.df.columns:
            self.df['Period Ending'] = pd.to_datetime(self.df['Period Ending'], errors='coerce')

        # 3. Formatear For Year como texto limpio para filtros
        if 'For Year' in self.df.columns:
            self.df['For Year Clean'] = self.df['For Year'].fillna(-1).astype(int).astype(str)
            self.df['For Year Clean'] = self.df['For Year Clean'].replace('-1', 'No Especificado')

    def get_info(self) -> pd.DataFrame:
        """Devuelve un resumen técnico de tipos de datos y valores nulos."""
        info_df = pd.DataFrame({
            'Tipo de Dato': self.df.dtypes.astype(str),
            'Valores No Nulos': self.df.notnull().sum(),
            'Valores Nulos': self.df.isnull().sum(),
            '% Nulos': (self.df.isnull().sum() / len(self.df) * 100).round(2)
        })
        return info_df

    def classify_variables(self) -> dict:
        """Clasifica las columnas del DataFrame en numéricas y categóricas."""
        num_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = self.df.select_dtypes(include=['object', 'category', 'datetime64[ns]']).columns.tolist()
        
        return {
            'numericas': num_cols,
            'categoricas': cat_cols,
            'total_num': len(num_cols),
            'total_cat': len(cat_cols)
        }

    def get_descriptive_stats(self) -> pd.DataFrame:
        """Calcula estadísticas descriptivas generales."""
        stats = self.df.describe().T
        stats['mediana'] = self.df.select_dtypes(include=[np.number]).median()
        stats['asimetria'] = self.df.select_dtypes(include=[np.number]).skew()
        return stats.round(2)

    def filter_data(self, tickers=None, years=None) -> pd.DataFrame:
        """Filtra el dataset dinámicamente según los parámetros del usuario."""
        filtered_df = self.df.copy()

        if tickers:
            filtered_df = filtered_df[filtered_df['Ticker Symbol'].isin(tickers)]

        if years:
            filtered_df = filtered_df[filtered_df['For Year Clean'].isin(years)]

        return filtered_df


# =========================================================
# NAVEGACIÓN Y ESTRUCTURA DE LA APLICACIÓN (Frontend Streamlit)
# =========================================================

# Menú lateral (Sidebar)
st.sidebar.title("📌 Menú de Navegación")
modulo = st.sidebar.radio(
    "Seleccione un Módulo:",
    ["1. Home (Presentación)", "2. Carga del Dataset", "3. Análisis Exploratorio (EDA)"]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Proyecto Aplicado - Python for Analytics**\nCaso de Estudio: NYSE")

# Estado global para mantener el analizador cargado en memoria
if 'analyzer' not in st.session_state:
    st.session_state['analyzer'] = None


# ---------------------------------------------------------
# MÓDULO 1: HOME
# ---------------------------------------------------------
if modulo == "1. Home (Presentación)":
    st.title("📈 Análisis Exploratorio de Datos: New York Stock Exchange (NYSE)")
    st.subheader("Especialización en Python for Analytics")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🎯 Objetivo del Proyecto
        Esta aplicación interactiva permite realizar un **Análisis Exploratorio de Datos (EDA)** exhaustivo sobre los estados financieros históricos de **448 empresas** de la Bolsa de Nueva York (NYSE).
        
        Evalúa métricas clave de:
        * **Ingresos y Rentabilidad:** Total Revenue, Net Income, Gross Margin, Profit Margin.
        * **Liquidez:** Current Ratio, Quick Ratio, Cash Ratio.
        * **Estructura Patrimonial:** Total Assets, Total Liabilities, Total Equity.
        * **Flujos de Efectivo:** Operating, Financing e Investing Cash Flows.
        
        ---
        ### 👨‍💻 Datos del Autor
        * **Nombre Completo:** Hugo Bazán Bravo
        * **Programa:** Especialización en Python for Analytics
        * **Institución:** DMC 
        * **Año:** 2026
        
        ---
        ### 🛠️ Tecnologías Utilizadas
        `Python 3.11` | `Pandas` | `NumPy` | `Matplotlib` | `Seaborn` | `Streamlit`
        """)
    
    with col2:
        st.image("https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?q=80&w=800", caption="Financial Analytics Dashboard")


# ---------------------------------------------------------
# MÓDULO 2: CARGA DEL DATASET
# ---------------------------------------------------------
elif modulo == "2. Carga del Dataset":
    st.title("📂 Carga del Dataset Financiero")
    st.write("Cargue el archivo en formato `.csv` para inicializar el motor de análisis POO.")

    uploaded_file = st.file_uploader("Seleccione el archivo 'New York Stock Exchange.csv'", type=["csv"])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state['analyzer'] = DataAnalyzer(df)
            st.success("✅ Archivo cargado y procesado exitosamente con la clase DataAnalyzer.")
            
            # Vista previa y métricas
            col1, col2 = st.columns(2)
            col1.metric("Total de Registros (Filas)", df.shape[0])
            col2.metric("Total de Variables (Columnas)", df.shape[1])

            st.markdown("### 🔍 Vista previa de los datos (`head`)")
            st.dataframe(df.head(10), use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error al procesar el archivo: {e}")
    else:
        st.warning("⚠️ Debe cargar el archivo CSV para habilitar el Módulo 3 de Análisis.")


# ---------------------------------------------------------
# MÓDULO 3: ANÁLISIS EXPLORATORIO DE DATOS (EDA)
# ---------------------------------------------------------
elif modulo == "3. Análisis Exploratorio (EDA)":
    st.title("📊 Análisis Exploratorio de Datos (EDA)")

    if st.session_state['analyzer'] is None:
        st.error("⚠️ No se ha cargado ningún dataset. Por favor diríjase primero al módulo '2. Carga del Dataset'.")
    else:
        analyzer = st.session_state['analyzer']

        # Pestañas (Tabs) para organizar los 10 ítems exigidos
        tabs = st.tabs([
            "Ítem 1: Info General",
            "Ítem 2: Clasificación",
            "Ítem 3: Est. Descriptiva",
            "Ítem 4: Datos Faltantes",
            "Ítem 5: Distribuciones",
            "Ítem 6: Categóricas",
            "Ítem 7: Bivariado (Num vs Cat)",
            "Ítem 8: Bivariado (Cat vs Cat)",
            "Ítem 9: Parámetros",
            "Ítem 10: Hallazgos Clave"
        ])

        # TAB 1: Información General
        with tabs[0]:
            st.header("Ítem 1: Información General del Dataset")
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Estructura y Registros Duplicados")
                st.write(f"**Registros duplicados totales:** {analyzer.df.duplicated().sum()}")
                st.dataframe(analyzer.get_info(), use_container_width=True)

            with col2:
                st.subheader("Observaciones Técnicas")
                st.markdown("""
                * La columna `Unnamed: 0` fue removida al funcionar solo como índice secundario.
                * `Period Ending` fue convertida correctamente al tipo `datetime`.
                * El dataset contiene 78 variables financieras operativas.
                """)

        # TAB 2: Clasificación
        with tabs[1]:
            st.header("Ítem 2: Clasificación de Variables")
            classif = analyzer.classify_variables()
            
            col1, col2 = st.columns(2)
            col1.metric("Variables Numéricas", classif['total_num'])
            col2.metric("Variables Categóricas / Fechas", classif['total_cat'])

            c1, c2 = st.columns(2)
            with c1:
                st.write("**Muestra de Variables Numéricas:**")
                st.write(classif['numericas'][:15])
            with c2:
                st.write("**Variables Categóricas:**")
                st.write(classif['categoricas'])

        # TAB 3: Estadística Descriptiva
        with tabs[2]:
            st.header("Ítem 3: Estadísticas Descriptivas")
            st.write("Resumen estadístico con medias, medianas, dispersión y asimetría:")
            st.dataframe(analyzer.get_descriptive_stats(), use_container_width=True)

        # TAB 4: Datos Faltantes
        with tabs[3]:
            st.header("Ítem 4: Análisis de Valores Faltantes")
            info_nulos = analyzer.get_info()
            nulos_df = info_nulos[info_nulos['Valores Nulos'] > 0]
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.dataframe(nulos_df)
            
            with col2:
                st.markdown("""
                ### 📌 Criterio y Discusión:
                * **Ratios de Liquidez:** Presentan 299 valores faltantes (16.79%). No se imputan por media/mediana para evitar distorsionar los perfiles de riesgo financiero reales.
                * **Earnings Per Share / Shares Outstanding:** Tienen 219 faltantes (12.29%).
                * **Conclusión:** Se conservan las ausencias documentadas sin imputación masiva.
                """)

        # TAB 5: Distribuciones Numéricas
        with tabs[4]:
            st.header("Ítem 5: Distribución de Variables Numéricas")
            
            col_metric = st.selectbox(
                "Seleccione una métrica financiera:",
                ["Total Revenue", "Net Income", "Total Assets", "Total Liabilities"]
            )
            
            escala = st.radio("Escala de visualización:", ["Millones ($M)", "Miles de Millones ($B)"], horizontal=True)
            divisor = 1e6 if escala == "Millones ($M)" else 1e9

            fig, ax = plt.subplots(figsize=(10, 4))
            sns.histplot(analyzer.df[col_metric] / divisor, kde=True, color="royalblue", ax=ax)
            ax.set_title(f"Distribución de {col_metric} ({escala})", fontsize=14)
            ax.set_xlabel(f"{col_metric} en {escala}")
            ax.set_ylabel("Frecuencia")
            st.pyplot(fig)

        # TAB 6: Variables Categóricas
        with tabs[5]:
            st.header("Ítem 6: Análisis de Variables Categóricas")
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.countplot(data=analyzer.df, x="For Year Clean", palette="viridis", ax=ax)
            ax.set_title("Cantidad de Registros Reportados por Año Fiscal (For Year)")
            ax.set_xlabel("Año Fiscal")
            ax.set_ylabel("Frecuencia")
            st.pyplot(fig)

        # TAB 7: Bivariado (Numérico vs Categórico)
        with tabs[6]:
            st.header("Ítem 7: Análisis Bivariado (Numérico vs Categórico)")
            
            top_n = st.slider("Seleccione el número de empresas Top por Ingresos:", 5, 20, 10)
            df_top = analyzer.df.groupby("Ticker Symbol")["Total Revenue"].mean().nlargest(top_n).reset_index()

            fig, ax = plt.subplots(figsize=(10, 4))
            sns.barplot(data=df_top, x="Ticker Symbol", y=df_top["Total Revenue"]/1e9, palette="mako", ax=ax)
            ax.set_title(f"Top {top_n} Empresas por Total Revenue Promedio ($B)")
            ax.set_ylabel("Ingresos Totales ($ Billones)")
            st.pyplot(fig)

        # TAB 8: Bivariado (Categórico vs Categórico)
        with tabs[7]:
            st.header("Ítem 8: Análisis Bivariado (Categórico vs Categórico)")
            
            # Categorización en rangos de Profit Margin
            analyzer.df['Profit_Margin_Cat'] = pd.qcut(
                analyzer.df['Profit Margin'], q=3, labels=['Bajo', 'Medio', 'Alto']
            )
            
            ct = pd.crosstab(analyzer.df['For Year Clean'], analyzer.df['Profit_Margin_Cat'], normalize='index') * 100
            
            fig, ax = plt.subplots(figsize=(8, 4))
            ct.plot(kind='bar', stacked=True, colormap='Spectral', ax=ax)
            ax.set_title("Distribución Porcentual del Margen de Utilidad por Año Fiscal")
            ax.set_ylabel("Porcentaje (%)")
            st.pyplot(fig)

        # TAB 9: Filtros Interactivos
        with tabs[8]:
            st.header("Ítem 9: Filtros Interactivos y Análisis Parametrizado")
            
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                tickers_sel = st.multiselect("Filtrar por Ticker Symbol:", options=sorted(analyzer.df['Ticker Symbol'].unique()))
            with col_f2:
                years_sel = st.multiselect("Filtrar por Año Fiscal:", options=sorted(analyzer.df['For Year Clean'].unique()))
            
            df_filtrado = analyzer.filter_data(tickers=tickers_sel, years=years_sel)
            st.write(f"**Registros coincidentes:** {len(df_filtrado)}")
            st.dataframe(df_filtrado[['Ticker Symbol', 'Period Ending', 'Total Revenue', 'Net Income', 'Total Assets']], use_container_width=True)

        # TAB 10: Hallazgos Clave
        with tabs[9]:
            st.header("Ítem 10: Hallazgos Clave y Recomendaciones")
            
            st.markdown("""
            ### 📌 Insights Principales derivados del EDA:
            1. **Sesgo Positivo Pronunciado:** Los *Total Revenue* y *Total Assets* exhiben una alta concentración en un número reducido de corporaciones líderes.
            2. **Solvencia General Saludable:** El *Current Ratio* promedio se mantiene en niveles adecuados (> 1.3), garantizando cobertura de deudas corrientes.
            3. **Aislación de Valores Faltantes:** Las ausencias no afectan los rubros contables principales (Balance y Estado de Resultados).
            4. **Estabilidad de Márgenes:** Los márgenes de utilidad se mantienen estables entre los años reportados salvo volatilidad puntual en sectores específicos.
            """)

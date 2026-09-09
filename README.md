# 📈 NYSE Financial Analytics - Exploratory Data Analysis (EDA)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://tu-aplicacion.streamlit.app)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)

## 📝 Descripción del Proyecto
Esta aplicación interactiva web fue desarrollada con **Streamlit** y **Python** para realizar un **Análisis Exploratorio de Datos (EDA)** exhaustivo sobre el estado financiero de empresas que cotizan en la **New York Stock Exchange (NYSE)**. 

El objetivo principal es examinar el desempeño financiero histórico mediante indicadores clave de ingresos, rentabilidad, liquidez, estructura de activos/pasivos y flujos de efectivo. La aplicación está construida aplicando principios de **Programación Orientada a Objetos (POO)** y ofrece una navegación modular por pestañas, filtros dinámicos por empresa/período y ajuste visual de escalas monetarias (miles, millones o miles de millones).

---

## 📸 Capturas de la Aplicación

<img width="567" height="266" alt="Home" src="https://github.com/user-attachments/assets/163d9d4a-93b8-443f-9d86-e37b3bc709c7" />

<img width="567" height="260" alt="Carga" src="https://github.com/user-attachments/assets/ac799b0f-7185-45d7-afd9-117b0a349d19" />

<img width="567" height="242" alt="Análisis EDA" src="https://github.com/user-attachments/assets/062c04d2-7984-4f41-95e8-4e0d63fa1888" />

---

## 🔗 Links Relevantes
* 🚀 **Aplicación Desplegada (Streamlit Cloud):** https://dmc61modulo2-hugobazan.streamlit.app/
* 📁 **Repositorio en GitHub:** https://github.com/hugobazan-mgmt/DMC61Modulo2/edit/main/README.md
* 🎓 **Institución:** Instituto DMC - Especialización en Python for Analytics

---

## 📊 Descripción Breve de las Variables Principales

El dataset abarca **1,781 registros** y **79 variables** correspondientes a **448 empresas**. A continuación, se detallan los campos métricos clave analizados:

* **`Ticker Symbol`**: Símbolo bursátil que identifica a la empresa en la bolsa.
* **`Period Ending`**: Fecha de cierre del ejercicio o período financiero.
* **`Total Revenue`**: Ingresos totales generados por la compañía en el período.
* **`Net Income`**: Utilidad o ganancia neta final disponible para la empresa.
* **`Total Assets`**: Activos totales (recursos y propiedades de la empresa).
* **`Total Liabilities`**: Pasivos totales (obligaciones y deudas financieras).
* **`Current Ratio`**: Razón corriente; indicador de liquidez a corto plazo ($Activo\ Corriente / Pasivo\ Corriente$).
* **`Quick Ratio`**: Prueba ácida; liquidez inmediata excluyendo inventarios.
* **`Profit Margin`**: Margen de utilidad; eficiencia para convertir ingresos en ganancias netas.
* **`For Year`**: Año fiscal reportado para el balance general y estado de resultados.

---

## 🛠️ Tecnologías y Librerías Utilizadas

* **Lenguaje:** Python 3.10+
* **Interfaz Web:** Streamlit (`st.sidebar`, `st.tabs`, `st.columns`, widgets interactivos)
* **Procesamiento de Datos:** Pandas, NumPy
* **Visualización:** Matplotlib, Seaborn
* **Arquitectura:** Programación Orientada a Objetos (Clase `DataAnalyzer` / `DataProcessor`)

---

## ⚙️ Instrucciones de Ejecución Local

Sigue estos pasos para clonar y ejecutar el proyecto en tu máquina local:

### 1. Clonar el repositorio
```bash
git clone [https://github.com/tu-usuario/nyse-eda-app.git](https://github.com/tu-usuario/nyse-eda-app.git)
cd nyse-eda-app

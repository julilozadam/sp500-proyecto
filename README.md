# sp500-proyecto
#ETL y Análisis de Empresas del S&P 500
## Descripción del Proyecto
Este proyecto tiene como objetivo analizar las empresas del S&P 500 a través de diferentes fases, que incluyen la extracción de datos, análisis estadístico, almacenamiento en SQL Server, creación de dashboards en Power BI, y finalmente, una clusterización basada en la volatilidad de las acciones.
## Requisitos
- Python 3.x
- Librerías: `pandas`, `sqlalchemy`, `pyodbc`, `scikit-learn`, `requests`, ` beautifulsoup4 `, `yfinance`, ` streamlit`, `seaborn`, ` matplotlib`, ` altair`, ` numpy`
- Power BI Desktop
- SQL Server

## Estructura del Proyecto
- `data/`: Contiene los archivos CSV con los datos de las empresas y
perfiles.
- Proyecto.py: Contiene el scripts Python para las fases 1, fase 3, fase 4.
- ETL_y_Clusterización_de_Empresas_del_S&P_500: Contiene el scripts de Python hecho en Google colab para la fase 5.
- BI proyecto: Contiene el archivo .pbix de Power BI.
- SQLQproyecto; Contiene el archivo .sql de la fase 3 del proyecto.
- `README.md`: Documento explicativo del proyecto.

## Instrucciones de Instalación y Uso
1. Clona este repositorio:
git clone https://github.com/tuusuario/sp500-proyecto.git
cd sp500-proyecto
2. Instala las dependencias necesarias:
pip install -r requirements.txt
3. Configura la conexión a SQL Server en los scripts de las fases
correspondientes.
4. Ejecuta los scripts en orden para realizar el análisis completo.
Fases del Proyecto
Fase 1: Extracción de Datos
• Obtención de datos de empresas del S&P 500 desde Wikipedia.
• Descarga de los precios de cotización del último año.
Fase 2: Análisis Estadístico
• Análisis descriptivo e inferencial de los precios de las acciones.
Fase 3: Almacenamiento en SQL Server
• Carga de los datos limpios en una base de datos SQL Server.
Fase 4: Dashboard en Power BI
• Creación de un dashboard interactivo con KPIs, tooltips y bookmarks.
Fase 5: Clusterización de las Acciones
• Agrupamiento de las acciones en clusters según indicadores de volatilidad.
Fase 6: Publicación en GitHub
• Subida del proyecto al repositorio de GitHub y documentación en este
archivo README.md.

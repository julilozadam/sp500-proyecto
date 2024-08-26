
import requests
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf
import os 
import logging
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import pyodbc


#EXTRACT

# a) Extraer la lista de empresas del S&P 500 desde Wikipedia

def get_response (url):
    try:
        logging.info(f"Se esta realizando la peticion para la siguiente URL: {url}")
        response = requests.get(url)
        logging.info(f"La peticion se proceso correctamente")
        return response
    except Exception as error:
        logging.error(f"Error procesando la peticion a la siguiente URL ({url}): {error}")

def get_soup(response):
    try:
        logging.info(f"Se esta parseando la informacion")
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except Exception as error:
        logging.error(f'Error al parsear la informacion: {error}')
    
 
def get_table(soup):
    try:
        logging.info(f'Se esta construyendo la tabla')
        table = soup.find('table', {'class': 'wikitable sortable'})
        return table
    except Exception as error:
        logging.error(f'Error al construir la tabla: {error}')
        

def get_companies(table): 
    try:
        logging.info(f'Se esta creando el dataframe de Companies')
        df_companies = pd.read_html(str(table))[0]
        return df_companies
    except Exception as error:
        logging.error(f'Error al construir el dataframe de companies: {error}')

# b) Obtener los precios de cada empresa desde Yahoo Finance

def get_prices (df_companies, start_date, end_date, tickers):
    try:
        logging.info(f"Simbolos obtenidos:{tickers}")
        logging.info(f"Rango de fechas definido: Desde {start_date} hasta {end_date}")
        prices = yf.download(tickers, start=start_date, end=end_date)['Close']
        logging.info("Datos descargados correctamente.")
        return prices
    except Exception as error:
        logging.error(f"Se produjo un error: {error}")
           


#TRANSFORM

# a) Limpiar los datos de la lista de empresas

def clean_datacompanies(df_companies, prices, tickers):
    try:
        logging.info(f'Se esta limpiando la informacion')
        df_companies_cleaned = df_companies.drop(columns=['Presentación ante la SEC', 'Sub-industria GICS', 'Fecha de incorporación','Clave de índice central',])
        df_companies_cleaned.rename(columns={'Símbolo': 'symbol', 'Seguridad': 'company' , 'Sector GICS':'sector', 'Ubicación de la sede':'headquarters', 'Fundada': 'fecha_fundada' }, inplace=True)
        logging.info(f'Se limpio la informacion')
        return df_companies_cleaned
    except Exception as error:
        logging.error(f"Se produjo un error: {error}")
        

# b) Limpiar los datos de los precios de las empresas

def clean_dataprices(prices,tickers):
    try:
        logging.info(f'Se esta limpiando la informacion')
        prices_cleaned= prices.drop(columns=['ABC'])
        prices_cleaned= prices.reset_index().melt(id_vars=["Date"], value_vars=tickers, var_name="Codigo empresa", value_name="Close")
        prices_cleaned=prices_cleaned.dropna()
        logging.info(f'Se limpio la informacion')
        return prices_cleaned
    except Exception as error:
        logging.error(f"Se produjo un error: {error}")


#LOAD

def create_dir(dir):
    try:
        logging.info(f'Se esta creando el directorio:{dir}')
        if not os.path.exists(dir):
            os.makedirs(dir)
            logging.info(f'Directorio creado')
        logging.info(f'El directorio ya existio')
    except Exception as error:
        logging.error(f"Se produjo un error creando el directorio: {error}")
            
    
 
# a) Guardar la lista de empresas transformada en un archivo CSV

def create_csv(df, name):
    try:
        logging.info(f'Se esta creando el csv para el dataframe: {df}')
        name= name+".csv"
        df.to_csv(name,encoding="utf-8-sig", index=False)
        logging.info('Se creo el dataframe')
    except Exception as error:
        logging.error(f"Se produjo un error creando el dataframe {error}")


#connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

def conection_sql_v2():
    connection_url = URL.create(
        "mssql+pyodbc",
        username="escribir el usuario",
        password="ezcribir contraseña",
        host="escribir el host",
        port=1433,
        database="STOCKS",
        query={
            "driver": "ODBC Driver 18 for SQL Server",
            "TrustServerCertificate": "yes",
            "authentication": "ActiveDirectoryIntegrated",
        },
    )

    # Crea la engine
    engine = create_engine(connection_url)
    return engine

def conection_sql():
    server = 'escribir el servidor'
    database = 'STOCKS'
    username = 'escribir usuario'
    password = 'escribir contraseña'
    driver = 'ODBC Driver 17 for SQL Server'

    # Construye la cadena de conexión
    connection_string = (
    f"mssql+pyodbc://{username}:{password}@{server}/{database}?"
    f"driver={driver.replace(' ', '+')};TrustServerCertificate=yes"
    )

    # Crea la engine
    engine = create_engine(connection_string)
    return engine

def load_data_to_sql(engine, df, table_name):
    try:
        df.to_sql(table_name, con=engine, index=False, if_exists='replace')
        print(f"Datos cargados correctamente en la tabla {table_name}")
    except Exception as e:
        print(f"Error al cargar datos en la tabla {table_name}:{e} ") 



def main():
    logging.basicConfig(filename='C:/Users/User/Documents/Talento Tech/Proyecto/Entrada proyecto/Proyecto/logs/etl_process.log', encoding='utf-8',level=logging.INFO, format='%(asctime)s -%(levelname)s - %(message)s')
    url = "https://es.wikipedia.org/wiki/Anexo:Compa%C3%B1%C3%ADas_del_S%26P_500"
    response = get_response(url)
    soup = get_soup(response)
    table = get_table(soup)
    df_companies = get_companies(table)
    start_date = pd.Timestamp.now() - pd.DateOffset(days=90)  # Último trimestre
    end_date = pd.Timestamp.now()
    tickers = df_companies['Símbolo'].tolist()
    prices = get_prices (df_companies, start_date, end_date, tickers)
    df_companies_cleaned = clean_datacompanies(df_companies, prices, tickers)
    prices_cleaned = clean_dataprices(prices,tickers)
    log_dir = './logs'
    data_dir = './data'
    create_dir(log_dir)
    create_dir(data_dir)
    os.chdir(data_dir)
    create_csv(df_companies_cleaned, "companies")
    create_csv(prices_cleaned, "prices")
    engine = conection_sql_v2()
    d = {'col1': [1, 2], 'col2': [3, 4]}
    df_companies_cleaned = pd.DataFrame(data=d)

    load_data_to_sql(engine, df_companies_cleaned, "companies")
    #load_data_to_sql(engine, prices_cleaned, "prices")
    
if __name__ == '__main__':
    main()


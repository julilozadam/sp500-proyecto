# -*- coding: utf-8 -*-
"""ETL y Clusterización de  Empresas del S&P 500.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1r2-Xg82azSKqNdkKBnnyqewGtfkOtAZB
"""

import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.tree import plot_tree
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import altair as alt
import streamlit as st

# from google.colab import files
# uploaded = files.upload ()

st.title('ETL y Clusterización de  Empresas del S&P 500')

st.write('Revision de los tipos de datos')
df = pd.read_csv('data\prices.csv')
df.head()

st.write(df.dtypes)

df['Date'] = pd.to_datetime(df['Date'])
st.write(df.dtypes)

df_sorted = df.sort_values(by=['Codigo empresa','Date'])
st.write(df_sorted.head())

st.write('Organizacion de la informacion por orden alfabetico')
df['return'] = df.groupby('Codigo empresa')['Close'].pct_change()*100
st.write(df.head())

df['return'] = df['return'].fillna(0)
st.write(df.head())

st.write(df[df['Codigo empresa']=='LUMN'])

st.write('Cálculo de Indicadores de Volatilidad')

stats_df = df.groupby('Codigo empresa')['return'].agg(['std', 'max', 'min', 'mean']).reset_index()

stats_df['range'] = stats_df['max'] - stats_df['min']

stats_df['mean_absolute'] = stats_df['mean'].abs()

stats_df.rename(columns={'std': 'std_return', 'max': 'max_return', 'min': 'min_return', 'mean': 'mean_return'}, inplace=True)

stats_df.drop(columns=['max_return','min_return','mean_return'], inplace = True)

st.write(stats_df)

#Normalizacion

st.write('Escalamiento de los Datos')

metrics = stats_df[['std_return', 'range', 'mean_absolute']]

scaler = StandardScaler()

scaled_metrics = scaler.fit_transform(metrics)

scaled_df = pd.DataFrame(scaled_metrics, columns=['std_return', 'range', 'mean_absolute'])

st.write(scaled_df.head())

st.write('Determinacion del número de clusters')

wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=42)
    kmeans.fit(scaled_df)
    wcss.append(kmeans.inertia_)

plt.figure(figsize=(10, 6))
plt.plot(range(1, 11), wcss, marker='o')
plt.title('Método del Codo')
plt.xlabel('Número de clusters')
plt.ylabel('WCSS')
plt.show()
st.pyplot(plt)

silhouette_scores = []
for i in range(2, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=42)
    cluster_labels = kmeans.fit_predict(scaled_df)
    silhouette_avg = silhouette_score(scaled_df, cluster_labels)
    silhouette_scores.append(silhouette_avg)

plt.figure(figsize=(10, 6))
plt.plot(range(2, 11), silhouette_scores, marker='o')
plt.title('Método de la Silueta')
plt.xlabel('Número de clusters')
plt.ylabel('Puntuación de la Silueta')
plt.show()
st.pyplot(plt)

st.write('Clusterización')

n_clusters = 3
kmeans = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=300, n_init=10, random_state=42)
stats_df['cluster'] = kmeans.fit_predict(scaled_df)

st.write(stats_df.head())

st.write(' Visualización de los Resultados')

# Graficar los clusters usando dos dimensiones para la visualización
plt.figure(figsize=(12, 8))
sns.scatterplot(x='std_return', y='range', hue='cluster', palette='viridis', data=stats_df, s=100, alpha=0.7)
plt.title('Clusters de Símbolos según Volatilidad')
plt.xlabel('Desviación Estándar de Retornos Diarios')
plt.ylabel('Rango de Retornos Diarios')
plt.legend(title='Cluster')
plt.show()
st.pyplot(plt)

"""#Conclusiones
1. Para calcular el número óptimo de clusters dado que se esta tratando con métricas estadísticas (desviación estándar, diferencia entre máximos y mínimos, etc.) derivadas de datos financieros, se hizo uso de los metodos del codo y de la silueta, el primera para una estimacion incial y el segundo para una evaluacion mas detallada de la calidad del clustering.

2. Observando el gráfico de los metodos empleados (silueta y codo), se puede ver que la puntuación de la silueta es máxima cuando K=3. Esto sugiere que, según este método, el número óptimo de clusters para tus datos es 3.

3. El gráfico muestra que las empresas pueden clasificarse en diferentes grupos según su nivel de volatilidad. Esta información es valiosa para los inversores, los gestores de riesgo y los analistas financieros.
Cluster de Baja Volatilidad: Las empresas en este cluster podrían ser grandes empresas establecidas en industrias maduras, estas empresas suelen tener una base de clientes estable y operaciones recurrentes, lo que contribuye a su menor volatilidad.
Cluster de Alta Volatilidad: Las empresas en este cluster suelen estar expuestas a mayores incertidumbres y cambios en el mercado, lo que se traduce en una mayor volatilidad.
Cluster Intermedio: Las empresas en este cluster podrían ser una mezcla de empresas de diferentes tamaños y sectores, que no encajan perfectamente en los otros dos clusters.

4.  El análisis de clusters de empresas según su volatilidad puede ser una herramienta invaluable para tomar decisiones financieras ya que pueden identificar segmentos de activos financieros que comparten características similares de volatilidad, por ejemplo los clusters que muestran alta volatilidad pueden indicar altos niveles de riesgo.

"""
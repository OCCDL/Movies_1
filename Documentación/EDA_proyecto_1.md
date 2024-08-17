# Documentación del Análisis de Películas

Este documento describe el proceso llevado a cabo para analizar un dataset de películas (`movies_credits3.csv`). El análisis incluye la visualización de una nube de palabras basada en los títulos de las películas, la identificación de las palabras más comunes, el análisis de los géneros de las películas y la exploración de la correlación entre diferentes variables numéricas.

## Librerías Utilizadas

- **pandas**: Para la manipulación de datos.
- **WordCloud**: Para la creación de nubes de palabras.
- **matplotlib**: Para la visualización de gráficos.
- **seaborn**: Para gráficos estadísticos avanzados.
- **nltk**: Para el procesamiento del lenguaje natural, en este caso, para el uso de stopwords.
- **numpy**: Para operaciones numéricas avanzadas.
- **collections.Counter**: Para contar la frecuencia de elementos en listas.

```python
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import seaborn as sns
import numpy as np
import nltk
from nltk.corpus import stopwords

1. Creación de Nube de Palabras basada en los Títulos de las Películas
Se concatenan todos los títulos de las películas en una única cadena de texto. Luego, se genera una nube de palabras para visualizar los términos más frecuentes.

df3 = pd.read_csv('movies_credits3.csv')

# Concatenar todos los títulos en una sola cadena de texto
all_titles = ' '.join(df3['title'].dropna())

# Crear la nube de palabras
wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate(all_titles)

# Mostrar la nube de palabras
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
Esta nube de palabras muestra las palabras más comunes en los títulos de las películas, proporcionando una representación visual del contenido del dataset.

2. Filtrado de Stopwords y Conteo de Frecuencia de Palabras
Se eliminan las palabras vacías o comunes (stopwords) en español y se cuentan las palabras más frecuentes en los títulos.

# Descargar stopwords en español
nltk.download('stopwords')

# Definir stopwords en español
stop_words = set(stopwords.words('spanish'))

# Dividir todos los títulos en palabras individuales y filtrar las stopwords
words = all_titles.split()
filtered_words = [word for word in words if word.lower() not in stop_words]

# Contar la frecuencia de cada palabra
word_freq = Counter(filtered_words)

# Convertir el resultado en DataFrame
df_word_freq = pd.DataFrame(word_freq.items(), columns=['word', 'frequency']).sort_values(by='frequency', ascending=False)

# Visualizar las 20 palabras más comunes
plt.figure(figsize=(10, 6))
sns.barplot(x='frequency', y='word', data=df_word_freq.head(20), palette='viridis')
plt.title('Top 20 palabras más comunes en los títulos')
plt.xlabel('Frecuencia')
plt.ylabel('Palabras')
plt.show()
Se muestra un gráfico de barras con las 20 palabras más comunes en los títulos de las películas, excluyendo las palabras vacías.

3. Análisis de Géneros de las Películas
Se realiza un análisis de los géneros de las películas, contando la frecuencia de aparición de cada género y visualizando los resultados en un gráfico.

# Rellenar valores NaN en la columna 'genres'
df3['genres'] = df3['genres'].fillna('')

# Contar la frecuencia de los géneros
all_genres = ' '.join(df3['genres']).replace('|', ' ').split()
genre_freq = Counter(all_genres)

# Convertir los géneros en DataFrame
df_genre_freq = pd.DataFrame(genre_freq.items(), columns=['genre', 'frequency']).sort_values(by='frequency', ascending=False)

# Visualizar la distribución de géneros
plt.figure(figsize=(10, 6))
sns.barplot(x='frequency', y='genre', data=df_genre_freq.head(10), palette='magma')
plt.title('Top 10 géneros de películas más comunes')
plt.xlabel('Frecuencia')
plt.ylabel('Género')
plt.show()
El gráfico muestra los 10 géneros más comunes en el dataset, ayudando a identificar qué tipo de películas son más frecuentes.

4. Análisis de Correlación entre Variables Numéricas
Se analizan las relaciones entre variables numéricas clave, como el presupuesto, los ingresos, el tiempo de duración, la popularidad, el promedio de votos y el número de votos, utilizando una matriz de correlación visualizada con un heatmap.

numeric_columns = ['budget', 'revenue', 'runtime', 'popularity', 'vote_average', 'vote_count']

# Crear una copia del DataFrame y convertir los valores 'sin dato' a NaN
df_temp = df3.copy()
df_temp[numeric_columns] = df_temp[numeric_columns].replace('sin dato', np.nan)
df_temp[numeric_columns] = df_temp[numeric_columns].astype(float)

# Calcular la matriz de correlación
correlation_matrix = df_temp[numeric_columns].corr()

# Visualizar la matriz de correlación
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Matriz de Correlación entre Variables Numéricas')
plt.show()
El heatmap muestra las correlaciones entre las variables numéricas del dataset, revelando posibles relaciones entre factores como el presupuesto y los ingresos.

5. Distribución de la Popularidad
Finalmente, se visualiza la distribución de la popularidad de las películas mediante un histograma.

# Histograma de popularidad
plt.figure(figsize=(8, 6))
sns.histplot(df3['popularity'], bins=20, kde=True)
plt.xlabel('Popularidad')
plt.ylabel('Frecuencia')
plt.title('Distribución de Popularidad')
plt.show()
El histograma proporciona una visión clara de cómo se distribuye la popularidad de las películas en el dataset.
# Documentación del Proceso de Fusión y Limpieza de Datos

Este documento explica de manera amigable el proceso de fusión y limpieza de dos conjuntos de datos relacionados con películas y sus créditos. Se describe cómo se procesaron los datos para prepararlos para análisis futuros. El código utiliza `pandas` y `re` para realizar las operaciones de limpieza y manipulación.

## Librerías Utilizadas
- `pandas`: Para la manipulación de los DataFrames.
- `re`: Para el manejo de expresiones regulares y filtrado de texto.

## Carga de los Archivos CSV

Primero, se cargan dos conjuntos de datos: `movies.modificado.csv` y `credits.modificado.csv`. Estos contienen información sobre películas y los créditos asociados.

```python
import pandas as pd
import re

df1_modicado = pd.read_csv('movies.modificado.csv')
df_credits2_modi = pd.read_csv('credits.modificado.csv')

Conversión de IDs a Strings
Para garantizar que ambos conjuntos de datos se puedan combinar correctamente, se convirtió la columna id en ambos DataFrames a tipo string.

df1_modicado['id'] = df1_modicado['id'].astype(str)
df_credits2_modi['id'] = df_credits2_modi['id'].astype(str)

Fusión de los Conjuntos de Datos
Los dos DataFrames se unieron utilizando una unión interna (inner join) basada en la columna id.

df_unidos = df1_modicado.merge(df_credits2_modi, how='inner', on='id')

Filtrado de Títulos con Caracteres Válidos
Se creó una función para verificar que los títulos contengan solo caracteres alfabéticos, números y algunos símbolos específicos. Luego, se filtraron los títulos inválidos en el DataFrame combinado.

def filtrar_titulo(titulo):
    return re.match(r"^[a-zA-Z0-9\s\$\-\#\?\&\!\ñ\¿\¡]*$", titulo) is not None

df_unidos = df_unidos[df_unidos['title'].apply(filtrar_titulo)]

Eliminación de Columnas Innecesarias
Se verificó la existencia de columnas irrelevantes (status, tagline, spoken_languages, production_countries) y se eliminaron del DataFrame.

columns_to_drop = ['status', 'tagline', 'spoken_languages', 'production_countries']
df_unidos = df_unidos.drop(columns=[col for col in columns_to_drop if col in df_unidos.columns], errors='ignore')


Manejo de Valores Nulos
Se reemplazaron los valores NaN en el DataFrame por la cadena 'sin dato' en las columnas donde se encontraron valores nulos.

df_unidos = df_unidos.apply(lambda x: x.fillna('sin dato') if x.isnull().any() else x)

Conversión de Tipos de Datos
Se aseguró que las columnas title, director_name y actor_names fueran de tipo string. Además, se verificó y ajustó el tipo de dato de la columna release_date para que sea de tipo datetime.

df_unidos['title'] = df_unidos['title'].astype(str)
df_unidos['director_name'] = df_unidos['director_name'].astype(str)
df_unidos['actor_names'] = df_unidos['actor_names'].astype(str)

if df_unidos['release_date'].dtype != 'datetime64[ns]':
    df_unidos['release_date'] = pd.to_datetime(df_unidos['release_date'], errors='coerce')

Guardado del DataFrame Procesado
Finalmente, el DataFrame resultante fue guardado en un nuevo archivo CSV para su uso posterior.

df_unidos.to_csv('movies_credits3.csv', index=False)

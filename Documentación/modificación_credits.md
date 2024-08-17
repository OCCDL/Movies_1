# Guía de Transformación y Limpieza de Datos en Dataset de Créditos de Películas

Esta guía explica el proceso realizado sobre un dataset de créditos de películas (`credits.csv`) para limpiar, transformar y desanidar columnas anidadas. La transformación incluye la eliminación de valores duplicados, el tratamiento de valores nulos, y la extracción de información relevante como el nombre del director y los actores principales. 

## Librerías Utilizadas

- **pandas**: Para la manipulación de datos.
- **re**: Para trabajar con expresiones regulares.
- **ast**: Para evaluar expresiones de cadenas a estructuras de datos en Python.

```python
import pandas as pd
import re
import ast

df_credits2 = pd.read_csv('credits.csv')

1. Contar y Eliminar Valores Duplicados y Nulos en la Columna id
Se verifica la existencia de valores duplicados y valores nulos en la columna id del dataset. Luego, se eliminan los duplicados manteniendo la primera ocurrencia.

# Contar valores duplicados y NaN en la columna 'id'
duplicados = df_credits2['id'].duplicated(keep=False).sum()
nan_count = df_credits2['id'].isna().sum()

# Eliminar duplicados en la columna 'id'
df_credits2 = df_credits2.drop_duplicates(subset='id', keep='first')

Este paso asegura que no existan valores duplicados ni nulos en la columna clave del dataset (id).

2. Conversión y Desanidamiento de la Columna crew
Se convierte la columna crew, que originalmente contiene texto, en una lista de diccionarios. A continuación, se extrae el nombre del director de cada película.

# Convertir la columna 'crew' a una lista de diccionarios
df_credits2['crew'] = df_credits2['crew'].apply(ast.literal_eval)

# Extraer el nombre del director
def extract_director(crew_list):
    for member in crew_list:
        if member.get('job') == 'Director':
            return member.get('name')
    return None

df_credits2['director_name'] = df_credits2['crew'].apply(extract_director)

Este paso facilita la extracción del nombre del director de cada película y lo coloca en una nueva columna director_name

3. Conversión y Desanidamiento de la Columna cast
Al igual que con crew, se convierte la columna cast en una lista de diccionarios, y se extraen los nombres de los actores.

# Convertir la columna 'cast' a una lista de diccionarios
df_credits2['cast'] = df_credits2['cast'].apply(ast.literal_eval)

# Extraer los nombres de los actores
def extract_actor_names(cast_list):
    return [member['name'] for member in cast_list if 'name' in member]

df_credits2['actor_names'] = df_credits2['cast'].apply(extract_actor_names)

Este paso permite obtener los nombres de los actores principales y almacenarlos en una nueva columna actor_names.

4. Eliminación de Columnas No Necesarias
Una vez que se han extraído los datos relevantes, se eliminan las columnas originales cast y crew para simplificar el dataset.

# Eliminar las columnas 'cast' y 'crew'
columns_to_drop = ['cast', 'crew']
df_credits2 = df_credits2.drop(columns=[col for col in columns_to_drop if col in df_credits2.columns], errors='ignore')

Esto optimiza el dataset al remover las columnas anidadas que ya no son necesarias.

5. Guardar el Dataset Modificado
El dataset transformado se guarda en un nuevo archivo CSV llamado credits.modificado.csv.

df_credits2.to_csv('credits.modificado.csv', index=False)

# Documentación de Transformación de Datos en Dataset de Películas

Este documento explica las operaciones realizadas sobre un dataset de películas, cuyo objetivo principal es limpiar, transformar y desanidar columnas anidadas en el DataFrame para facilitar el análisis posterior. El código se implementa en Python utilizando la librería `pandas`.

## Librerías Utilizadas

- **pandas**: Para la manipulación y análisis de datos.
- **re**: Para el uso de expresiones regulares.
- **ast**: Para evaluar cadenas de texto y convertirlas a objetos.

## Paso 1: Carga del Dataset

El dataset `movies_dataset.csv` se carga en un DataFrame de `pandas`. Además, se configura `pandas` para mostrar todas las columnas del DataFrame.

```python
df1 = pd.read_csv('movies_dataset.csv')
pd.set_option('display.max_columns', None)

Paso 2: Desanidamiento de Columnas
Columna belongs_to_collection
Se desanida la columna belongs_to_collection para extraer los valores de los campos id y name. Estos se almacenan en las nuevas columnas coll_id y coll_name, respectivamente.

df1['coll_id'] = df1['belongs_to_collection'].str.extract(r"'id': ([^,]*)", flags=re.IGNORECASE)
df1['coll_name'] = df1['belongs_to_collection'].str.extract(r"'name': '([^']*)", flags=re.IGNORECASE)

Columna production_companies
Se desanidan los valores de id y name de la columna production_companies en las nuevas columnas production_company_id y production_company_name.

df1['production_company_id'] = df1['production_companies'].str.extract(r"'id': ([^}]*)", flags=re.IGNORECASE)
df1['production_company_name'] = df1['production_companies'].str.extract(r"'name': '([^']*)", flags=re.IGNORECASE)

Paso 3: Relleno de Valores Nulos
Se cuentan y rellenan los valores nulos en las columnas revenue y budget con ceros (0).

df1['revenue'] = df1['revenue'].fillna(0)
df1['budget'] = df1['budget'].fillna(0)

Paso 4: Eliminación de Valores Nulos en release_date
Se eliminan los registros donde la columna release_date contiene valores nulos.

df1 = df1.dropna(subset=['release_date'])

Paso 5: Extracción del Año de Lanzamiento
Se convierte la columna release_date a formato de fecha y se extrae el año de lanzamiento en una nueva columna llamada release_year.

df1['release_date'] = pd.to_datetime(df1['release_date'], errors='coerce').dt.strftime('%Y-%m-%d')
df1['release_year'] = pd.to_datetime(df1['release_date'], errors='coerce').dt.year.astype('Int64')

Paso 6: Creación de la Columna return
Se calcula la columna return dividiendo revenue entre budget. Si el presupuesto es 0, se asigna un valor de 0 a la columna.

df1['return'] = df1.apply(lambda row: row['revenue'] / row['budget'] if row['budget'] != 0 else 0, axis=1)

Paso 7: Eliminación de Columnas
Se eliminan columnas irrelevantes como video, imdb_id, adult, original_title, poster_path, homepage y otras sugeridas.

columns_to_remove = ['video', 'imdb_id', 'adult', 'original_title', 'poster_path', 'homepage']
df1.drop(columns=columns_to_remove, inplace=True)

Se eliminan también las columnas belongs_to_collection y production_companies.

df1 = df1.drop(columns=['belongs_to_collection', 'production_companies'], errors='ignore')

Paso 8: Desanidamiento de la Columna genres
Se desanida la columna genres, extrayendo los géneros como una cadena separada por comas.

def extract_genres(genres_list):
    if isinstance(genres_list, list) and genres_list:
        genres = [genre['name'] for genre in genres_list if 'name' in genre]
        return ', '.join(genres)
    return ''

df1['genres'] = df1['genres'].apply(lambda x: extract_genres(ast.literal_eval(x)) if pd.notna(x) and x != 'NaN' else '')

Paso 9: Eliminación de Duplicados y Valores Nulos en id
Se cuentan y eliminan los valores duplicados en la columna id, manteniendo solo la primera ocurrencia. Además, se eliminan los valores nulos.

df1 = df1.drop_duplicates(subset='id', keep='first')

Paso 10: Guardado del DataFrame Modificado
Finalmente, se guarda el DataFrame modificado en un nuevo archivo CSV llamado movies.modificado.csv.

df1.to_csv('movies.modificado.csv', index=False)

Este proceso asegura que el dataset esté limpio y listo para análisis posteriores, con todas las columnas anidadas desglosadas y los valores nulos tratados correctamente.
from fastapi import FastAPI, HTTPException
import pandas as pd
import uvicorn
import ast
from typing import Dict, List, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



# Lea el archivo CSV que contiene el conjunto de datos de la película y guárdelo en un DataFrame con una URL de Google Drive
url = 'https://drive.google.com/file/d/1_5nnz8J0uJxDymdPgoRvUzyFYC6qCLqg/view?usp=sharing'

url='https://drive.google.com/uc?id=' + url.split('/')[-2]

data = pd.read_csv(url) 



# https://drive.google.com/file/d/1_5nnz8J0uJxDymdPgoRvUzyFYC6qCLqg/view?usp=sharing
# data = pd.read_csv('data/movies_credits3.csv')

app = FastAPI()

@app.get("/cantidad_filmaciones_mes/{mes}")
async def cantidad_filmaciones_mes(mes: str):
    # Convertir la columna 'release_date' a formato datetime (si no está en ese formato)
    data['release_date'] = pd.to_datetime(data['release_date'], errors='coerce')
    
    # Mapeo de los nombres de meses en español a sus respectivos números
    meses_nombres = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
        'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
        'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }

    # Convertir el nombre del mes a su correspondiente número
    mes_num = meses_nombres.get(mes.lower(), None)
    
    # Validación si es un nombre de mes o un número
    if mes_num is None:
        try:
            mes_num = int(mes)
            if mes_num < 1 or mes_num > 12:
                raise ValueError
        except ValueError:
            raise HTTPException(status_code=400, detail="El mes ingresado no es válido")

    # Filtrar las películas por el mes especificado
    cantidad = data[data['release_date'].dt.month == mes_num].shape[0]

    # Devolver la cantidad de películas
    return {"mes": mes.capitalize(), "cantidad": cantidad}


@app.get("/cantidad_filmaciones_dia/{dia}")
async def cantidad_filmaciones_dia(dia: str):
    # Convertimos la columna 'release_date' a formato datetime si no lo está.
    if not pd.api.types.is_datetime64_any_dtype(data['release_date']):
        data['release_date'] = pd.to_datetime(data['release_date'])

    # Mapeo de nombres de días en español a sus respectivos números.
    dias_nombres = {
        'lunes': 0, 'martes': 1, 'miércoles': 2, 'jueves': 3,
        'viernes': 4, 'sábado': 5, 'domingo': 6
    }

    # Convertimos el día a minúscula y verificamos si es un nombre de día válido.
    dia = dia.lower()
    dia_num = dias_nombres.get(dia)
    if dia_num is None:
        raise HTTPException(status_code=400, detail="El día ingresado no es válido")

    # Filtramos las películas por el día especificado.
    cantidad = data[data['release_date'].dt.dayofweek == dia_num].shape[0]

    # Devolvemos la cantidad de películas.
    return {"día": dia.capitalize(), "cantidad": cantidad}


@app.get("/score_titulo/{titulo_de_la_filmacion}")
async def score_titulo(titulo_de_la_filmacion: str):
    # Filtrar el DataFrame por el título ingresado
    pelicula = data[data['title'].str.lower() == titulo_de_la_filmacion.lower()]

    # Verificar si la película existe
    if pelicula.empty:
        raise HTTPException(status_code=404, detail="Película no encontrada")

    # Extraer el título, año de estreno y score
    titulo = pelicula['title'].values[0]
    año_estreno = pelicula['release_date'].dt.year.values[0]
    score = pelicula['popularity'].values[0]  

    # Retornar la respuesta en el formato solicitado
    return {
        "mensaje": f"La película {titulo} fue estrenada en el año {año_estreno} con un score/popularidad de {score}"
    }


@app.get("/votos_titulo/{titulo_de_la_filmacion}")
async def votos_titulo(titulo_de_la_filmacion: str):
    # Filtrar el DataFrame por el título ingresado
    pelicula = data[data['title'].str.lower() == titulo_de_la_filmacion.lower()]

    # Verificar si la película existe
    if pelicula.empty:
        raise HTTPException(status_code=404, detail="Película no encontrada")

    # Extraer el título, cantidad de votos y valor promedio
    titulo = pelicula['title'].values[0]
    votos = pelicula['vote_count'].values[0]
    promedio = pelicula['vote_average'].values[0]

    # Verificar si la cantidad de votos es suficiente
    if votos < 2000:
        raise HTTPException(status_code=400, detail="La película no tiene suficientes valoraciones")

    # Retornar la respuesta en el formato solicitado
    return {
        "mensaje": f"La película {titulo} fue estrenada en el año {pelicula['release_date'].dt.year.values[0]}. La misma cuenta con un total de {votos} valoraciones, con un promedio de {promedio}"
    }
    
    
    
@app.get("/get_actor/{nombre_actor}")
async def get_actor(nombre_actor: str):
    # Filtrar el DataFrame para obtener las películas en las que ha participado el actor
    peliculas_actor = data[data['actor_names'].apply(lambda x: nombre_actor.lower() in [actor.lower() for actor in ast.literal_eval(x)])]

    # Verificar si el actor ha participado en alguna película
    if peliculas_actor.empty:
        raise HTTPException(status_code=404, detail="Actor no encontrado en el dataset")

    # Calcular el total de retorno y el promedio
    total_retorno = peliculas_actor['revenue'].sum()
    promedio_retorno = peliculas_actor['revenue'].mean()
    cantidad_peliculas = peliculas_actor.shape[0]

    # Retornar la respuesta en el formato solicitado
    return {
        "mensaje": (
            f"El actor {nombre_actor} ha participado en {cantidad_peliculas} películas, "
            f"con un retorno total de {total_retorno} y un promedio de retorno de {promedio_retorno:.2f} por película."
        )
    }
    
    
@app.get('/get_director/{nombre_director}')
def get_director(nombre_director: str) -> Dict[str, Any]:
    # Filtrar el DataFrame por el nombre del director
    director_df = data[data['director_name'].str.contains(nombre_director, na=False)]
    
    if director_df.empty:
        return {"success": False, "message": "No se encontraron películas para el director especificado."}
    
    peliculas = []
    for _, row in director_df.iterrows():
        pelicula = {
            "title": row['title'],
            "release_date": row['release_date'],
            "return": row['return'],
            "budget": row['budget'],
            "revenue": row['revenue']
        }
        peliculas.append(pelicula)
    
    return {
        "success": True,
        "director": nombre_director,
        "peliculas": peliculas
    }
    
    
@app.get("/recomendacion/{titulo}")
async def obtener_recomendacion(titulo: str, top_n: int = 5):
    # Convertir tanto el título ingresado como los títulos en el DataFrame a minúsculas para una comparación insensible a mayúsculas/minúsculas
    titulo = titulo.lower()
    data['title_lower'] = data['title'].str.lower()

    # Verificar si el título existe en el DataFrame
    if titulo not in data['title_lower'].values:
        # Devolver un mensaje de error si no se encuentra la película
        return {"Error": "Película no encontrada"}

    # Obtener el índice de la película especificada
    idx = data.index[data['title_lower'] == titulo].tolist()[0]

    # Extraer las descripciones (overview) de todas las películas
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')

    # Ajustar y transformar las descripciones (overview)
    tfidf_matrix = tfidf_vectorizer.fit_transform(data['overview'].fillna(''))

    # Calcular la similitud del coseno entre la película seleccionada y todas las demás
    cosine_sim = cosine_similarity(tfidf_matrix[idx], tfidf_matrix)

    # Obtener las puntuaciones de similitud y ordenar por la más alta
    sim_scores = list(enumerate(cosine_sim[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Excluir la primera película (es la misma) y obtener las top_n más similares
    sim_scores = sim_scores[1:top_n + 1]

    # Obtener los índices de las películas recomendadas
    movie_indices = [i[0] for i in sim_scores]

    # Devolver los títulos de las películas recomendadas
    recomendaciones = data['title'].iloc[movie_indices].tolist()

    # Devolver la lista de películas recomendadas
    return {"lista_recomendada": recomendaciones}



# Esta línea verifica si este script se está ejecutando directamente (en lugar de importarse como un módulo en otro script).
if __name__ == "__main__":
    # Si el script se ejecuta directamente, utiliza el servidor ASGI 'uvicorn' para servir a la aplicación FastAPI. Se ejecuta en la máquina local (host="0.0.0.0") en el puerto 8000.
    # 'reload=True' habilita la recarga en caliente, lo que significa que el servidor se actualizará automáticamente cada vez que se realice un cambio en el script.
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=True)
    


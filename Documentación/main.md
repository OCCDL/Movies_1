# API de Películas - Documentación

Esta API está diseñada para proporcionar diversas funcionalidades relacionadas con películas, tales como consultas de datos de filmaciones, popularidad, recomendaciones, y más. La aplicación está construida utilizando FastAPI y procesa un conjunto de datos (`movies_credits3.csv`) que contiene información sobre películas.

## Endpoints Disponibles

### `/cantidad_filmaciones_mes/{mes}`
**Descripción**: Este endpoint devuelve la cantidad de películas estrenadas en un mes específico.

- **Parámetro**: `mes` (str) - Nombre o número del mes (Ej. "enero" o "1").
- **Retorno**: Un objeto JSON con el nombre del mes y la cantidad de películas estrenadas en dicho mes.
- **Errores**:
  - `400`: Mes no válido.
  
### `/cantidad_filmaciones_dia/{dia}`
**Descripción**: Devuelve la cantidad de películas estrenadas en un día de la semana específico.

- **Parámetro**: `dia` (str) - Nombre del día en español (Ej. "lunes", "martes").
- **Retorno**: Un objeto JSON con el día y la cantidad de películas estrenadas en ese día.
- **Errores**:
  - `400`: Día no válido.

### `/score_titulo/{titulo_de_la_filmacion}`
**Descripción**: Devuelve información sobre el título de una película, incluyendo el año de estreno y el score de popularidad.

- **Parámetro**: `titulo_de_la_filmacion` (str) - El título de la película.
- **Retorno**: Un mensaje con el título, año de estreno y el score/popularidad de la película.
- **Errores**:
  - `404`: Película no encontrada.

### `/votos_titulo/{titulo_de_la_filmacion}`
**Descripción**: Proporciona la cantidad de votos y el promedio de valoración para una película.

- **Parámetro**: `titulo_de_la_filmacion` (str) - El título de la película.
- **Retorno**: Un mensaje con el número de votos, el promedio y el año de estreno.
- **Errores**:
  - `404`: Película no encontrada.
  - `400`: No tiene suficientes valoraciones.

### `/get_actor/{nombre_actor}`
**Descripción**: Devuelve información sobre las películas en las que ha participado un actor específico, incluyendo el total y el promedio de retorno.

- **Parámetro**: `nombre_actor` (str) - Nombre del actor.
- **Retorno**: Un mensaje con el número de películas, el retorno total y el promedio por película.
- **Errores**:
  - `404`: Actor no encontrado en el dataset.

### `/get_director/{nombre_director}`
**Descripción**: Muestra información sobre las películas dirigidas por un director en particular.

- **Parámetro**: `nombre_director` (str) - Nombre del director.
- **Retorno**: Una lista de películas dirigidas por el director, con detalles como título, fecha de estreno, presupuesto, retorno y ganancias.
- **Errores**:
  - Si no se encuentra ninguna película dirigida por el director, se devuelve un mensaje indicando esto.

### `/recomendacion/{titulo}`
**Descripción**: Devuelve una lista de películas recomendadas basadas en la similitud de descripciones (overview) con la película especificada.

- **Parámetro**: `titulo` (str) - Título de la película.
- **Parámetro Opcional**: `top_n` (int) - Número de recomendaciones a devolver (valor por defecto: 5).
- **Retorno**: Una lista de títulos de películas recomendadas.
- **Errores**:
  - `Error`: Si la película no se encuentra en el dataset.

## Funcionamiento Interno
El API se conecta a un dataset de películas y utiliza bibliotecas como `pandas` para la manipulación de datos, y `scikit-learn` para cálculos de similitud basados en TF-IDF y similitud coseno. Cada endpoint utiliza lógica para filtrar y analizar datos de acuerdo con los parámetros ingresados por el usuario.

El código también maneja excepciones de manera robusta para asegurar que se devuelvan mensajes de error claros en casos de entradas inválidas o datos no encontrados.



# Sistema de recomendación de películas


![Project Image](https://drive.google.com/uc?export=view&id=1umgajnd50xS4dlKIB7y2xzMraXRtT0t-)

Este sistema de recomendación de películas está diseñado para ofrecerte una experiencia rápida y eficiente a la hora de encontrar nuevas películas para ver. Utilizando un extenso dataset de películas, el sistema analiza las similitudes entre títulos para sugerirte opciones relevantes basadas en una película de tu elección. Simplemente ingresa el nombre de una película que disfrutes, y el sistema te proporcionará recomendaciones personalizadas.
##  Índice
1. [Proceso de preparación y limpieza de datos](#cleaning)
2. [Análisis exploratorio de datos](#eda)
3. [Modelo de recomendación](#model)
4. [Documentación](#documentation)
5. [Cómo usar](#use)
6. [Ejemplo de uso](#example)
7. [Dependencias](#dependencies)

##  1. Proceso de preparación y limpieza de datos 

El primer paso de nuestro proyecto es la limpieza y preparación de los datos. En este paso, normalizamos y limpiamos nuestro conjunto de datos para su posterior análisis y modelado.

##  2. Análisis exploratorio de datos (EDA) 

Una vez que los datos están limpios y preparados, realizamos un EDA para descubrir patrones, tendencias y relaciones en los datos. 

##  3. Modelo de recomendación 

Usamos el análisis de los datos para construir nuestro sistema de recomendaciones, que proporciona sugerencias de películas basadas en un título de película especificado por el usuario. 

##  4. Documentación 

En esta sección, encontrará documentación relacionada con diferentes aspectos del proyecto. A continuación, se enumeran cada archivo de documentación y su descripción:

- [Modificación movies(ETL1)](Documentación/modificación_movies.md): Documentación sobre el proceso de extracción, transformación y carga (ETL1). Explica cómo se preparó y limpió el conjunto de datos de la película.

- [Modificación credits(ETL2)](Documentación/modificación_credits.md): Documentación sobre el proceso de extracción, transformación y carga (ETL2). Explica cómo se preparó y limpió el conjunto de datos de la película.

- [EDA](Documentación/EDA_proyecto_1.md): Documentación sobre el proceso de análisis exploratorio de datos (EDA). Describe los pasos y las técnicas que se utilizan para explorar y comprender el conjunto de datos de la película.

- [Unir tablas](Documentación/unir_tablas.md): Documentación sobre el proceso que se utilizo para terminar de modificar y al final unir las tablas ya modificadas y guardar el ultimo archivo.csv

- [main](Documentación/main.md): Documentación sobre el modelo de recomendación utilizado en el proyecto. Describe el algoritmo utilizado, las características de entrada y cómo se generan las recomendaciones.

*Puede acceder a cada archivo de documentación haciendo clic en cada uno de los nombres de archivo correspondientes*

##  5. Cómo usar <a name="use"></a>

Los usuarios pueden interactuar con la API visitando el servidor en su navegador y proporcionando el título de una película. La API devolverá una lista de películas recomendadas según el título proporcionado.

##  6. Ejemplo de uso <a name="example"></a>

Para obtener recomendaciones de películas, visite el servidor en su navegador y proporcione el título de una película. La API devolverá una lista de películas recomendadas.



## ⚙️ 7. Dependencias <a name="dependencies"></a>

El proyecto depende de las siguientes bibliotecas:
- pandas
- numpy
- seaborn
- matplotlib
- sklearn
- FastAPI
- Uvicorn
- wordcloud

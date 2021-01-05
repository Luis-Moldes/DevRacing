# DevRacing
Proyecto de prueba para Devaway. Capaz de importar información en formato JSON, tratarla y ofrecer una serie de clasificaciones y resultados.


## Overview
El funcionamiento básico de la API es el siguiente: la información se importa a la base de datos mediante un método POST que incluye en su *body* la información a guardar. A partir de este momento, la API es capaz de devolver mediante métodos GET cada uno de los análisis requeridos en el guión de la prueba técnica:

- Clasificación general de todas las carreras (Piloto - Tiempo total - Puntos)
- Clasificación general de una carrera en concreto (Piloto - Tiempo total - Mejor vuelta - Puntos)
- Datos de un piloto en concreto. (Carrera - Tiempo total - Mejor vuelta - Puntos)

El procedimiento exacto para cada uno de estos métodos se describirá individualmente a continuación endpoint por endpoint, después de describir los primeros pasos para runnear el development server mediante Python y Django.

Al respecto del funcionamiento interno de la API, si se requiere una descripción detallada del código lo conveniente sería discutirlo mediante una entrevista, dado que son untilizadas algunas particularidades de Django REST con las que el lector puede no estar familiarizado. Para dar una visión global, al introducir los datos se crean y almacenan una serie de objetos "Piloto", los cuales contienen toda la información necesaria para cada uno de los endpoints, los cuales al ser llamados los inspeccionan de la manera adecuada y ofrecen la información al usuario en forma de JSON.
 
 
## Procesos preliminares

## Métodos
### Subir datos
URL:
Método:
Datos a incluir:

Descripción:

Output (en caso de éxito):


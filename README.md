# DevRacing
Proyecto de prueba para Devaway. Capaz de importar información en formato JSON, tratarla y ofrecer una serie de clasificaciones y resultados.


## Overview
El funcionamiento básico de la API es el siguiente: la información se importa a la base de datos mediante un método POST que incluye en su *body* la información a guardar. A partir de este momento, la API es capaz de devolver mediante métodos GET cada uno de los análisis requeridos en el guión de la prueba técnica:

- Clasificación general de todas las carreras (Piloto - Tiempo total - Puntos)
- Clasificación general de una carrera en concreto (Piloto - Tiempo total - Mejor vuelta - Puntos)
- Datos de un piloto en concreto. (Carrera - Tiempo total - Mejor vuelta - Puntos)

El procedimiento exacto para cada uno de estos métodos se describirá individualmente a continuación endpoint por endpoint, después de describir los primeros pasos para runnear el development server mediante Python y Django.

Al respecto del funcionamiento interno de la API, si se requiere una descripción detallada del código lo conveniente sería discutirlo mediante una entrevista, dado que son untilizadas algunas particularidades de Django REST con las que el lector puede no estar familiarizado. Para dar una visión global, al introducir los datos se crean y almacenan una serie de objetos "Piloto", los cuales, tras los cálculos de tiempos y puntos correspondientes, contienen toda la información necesaria para cada uno de los endpoints, los cuales al ser llamados los inspeccionan de la manera adecuada y ofrecen la información al usuario en forma de JSON.
 
 
## Procesos preliminares

En primer lugar, se deben añadir al compilador las librerías recogidas en el archivo *requirements.txt*. Esto se puede realizar de forma conveniente mediante el comando
```
pip install -r requirements.txt
```

Una vez instalados, se debería poder utilizar el archivo *manage.py* para interactuar con la API. De esta manera, se puede activar la API mediante el comando
```
python manage.py runserver
```

A partir de ahí, el servidor local estará en línea, generalmente en la URL http://127.0.0.1:8000/ (en la descripción de cada método, esta dirección será omitida mediante "..."), pudiéndose mandar *requests* a todos sus endopints mediante el método que más cómodo resulte.

## Métodos
### Subir datos
**URL**: .../post-data/

**Método**: POST

**Datos a incluir**: La información a añadir a la base de datos, con formato JSON en el *body* de la *request* (seleccionando la opción *raw JSON*)

**Descripción**: La información es añadida a la base de datos, de forma que el resto de métodos puedan acceder a ella. La API es además capaz de detectar si los datos que se intentan subir ya se encuentran en la base de datos, advirtirndo al usuario de ello y evitando que estos datos queden duplicados.

**Output (en caso de éxito)**: Mensaje informando de la cantidad de pilotos y carreras añadidos a la base de datos.

### Eliminar datos
**URL**: .../post-data/

**Método**: DELETE

**Datos a incluir**: Ninguno

**Descripción**: Se elimina toda la información de la base de datos

**Output (en caso de éxito)**: *"Todos los datos han sido eliminados"*

### Consultar piloto
**URL**: .../get-pilot/?name=*piloto a consultar*

**Método**: GET

**Datos a incluir**: Nombre del piloto a consultar, como parte de la URL (p.ej. http://127.0.0.1:8000/get-pilot/?name=Cooke Rivers) o en los *query parameters* de la *request* (KEY=name, VALUE=Cooke Rivers) (ambos métodos son equivalentes)

**Descripción**: Devuelve, en formato JSON, la información requerida al respecto de todas las carreras del piloto seleccionado (añadiendo además su posición en cada una de ellas). A su vez, la API informa adecuadamente en caso de que el piloto no figure en la base de datos, así como del caso en que la base de datos esté completamente vacía.

**Output (en caso de éxito)**:
```
{
    "Nombre": "Cooke Rivers",
    "ID": "5fd7dbd8ce3a40582fb9ee6b",
    "Edad": 23,
    "Equipo": "PROTODYNE",
    "Foto": "http://placehold.it/64x64",
    "Carreras": {
        "Race 0": {
            "Posición": 13,
            "Puntos": 0,
            "Tiempo Total": "1:50:41.257000",
            "Mejor Vuelta": "0:08:04.951000"
        },
        "Race 1": {
            "Posición": 12,
            "Puntos": 0,
            "Tiempo Total": "1:50:08.934000",
            "Mejor Vuelta": "0:08:12.974000"
        },
        ...
 }
```

### Consultar carrera
**URL**: .../get-race/?name=*carrera a consultar*

**Método**: GET

**Datos a incluir**: Nombre de la carrera a consultar, como parte de la URL (p.ej. http://127.0.0.1:8000/get-race/?name=Race 1) o en los *query parameters* de la *request* (KEY=name, VALUE=Race 1) (ambos métodos son equivalentes)

**Descripción**: Devuelve, en formato JSON, la información requerida al respecto de la actuación en la carrera seleccionada de todos los pilotos presentes en la base de datos (ordenados por su posición en la misma). A su vez, la API informa adecuadamente en caso de que la carrera no figure en la base de datos, así como del caso en que la base de datos esté completamente vacía.

**Output (en caso de éxito)**:
```
[
    {
        "Nombre": "Kitty Farmer",
        "Datos de su carera": {
            "Posición": 1,
            "Puntos": 25,
            "Tiempo Total": "1:41:10.653000",
            "Mejor Vuelta": "0:08:01.389000"
        }
    },
    {
        "Nombre": "Merle Rhodes",
        "Datos de su carera": {
            "Posición": 2,
            "Puntos": 18,
            "Tiempo Total": "1:41:59.213000",
            "Mejor Vuelta": "0:08:10.802000"
        }
    },
    ...
]
```

### Consultar clasificación general
**URL**: .../get-list-all/

**Método**: GET

**Datos a incluir**: Ninguno

**Descripción**: Devuelve la clasificación de todos los pilotos tras el cómputo de los puntos obtenidos en cada una de sus carreras, así como la información adicional requerida para cada uno de ellos.

**Output (en caso de éxito)**:
```
[
    {
        "name": "White Elliott",
        "total_time": "17:51:21.571000",
        "total_pts": 90
    },
    {
        "name": "Kitty Farmer",
        "total_time": "17:54:10.571000",
        "total_pts": 81
    },
    {
        "name": "Cotton Sosa",
        "total_time": "18:10:56.603000",
        "total_pts": 77
    },
    ...
]
```


# El objetivo de este fichero es generar una NUEVA IMAGEN DE CONTENEDOR... para mi proyecto

# Preparar el entorno que necesito.
## Partiendo de una imagen que ya tenga preinstalado python 3.12
FROM python:3.12
## Copio un fichero que incluye las dependencias que tiene mi proyecto
COPY requirements.txt /tmp/requirements.txt
## Solicito la instalación de esas dependencias
RUN pip install --no-cache-dir -r /tmp/requirements.txt


# Configuro mi ejecución

## Defino unas variables de entorno para mi contenedor
ENV RUTA_DATOS=/datos
ENV RUTA_DESTINO_MODELO=/exportacion

## Defino unos volumenes para mi contenedor
VOLUME ["/datos"]
VOLUME ["/exportacion"]

## Establezco que cuando un comando sea ejecutado en este contenedor, por defecto se ejecute en la carpeta /modelo
WORKDIR /modelo


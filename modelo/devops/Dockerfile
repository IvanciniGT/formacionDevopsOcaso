# El objetivo de este fichero es generar una NUEVA IMAGEN DE CONTENEDOR... para mi proyecto

# Preparar el entorno que necesito.
## Partiendo de una imagen que ya tenga preinstalado python 3.12
FROM python:3.12
# Cuando este fichero se ejecuta... a través del comando "docker build"
# Docker lo que hará es CREAR UN CONTENEDOR TEMPORAL desde esa imagen de contenedor (FROM)

## En ese contenedor temporal, es donde copio un fichero que incluye las dependencias que tiene mi proyecto
COPY requirements.txt /tmp/requirements.txt

## Solicito la instalación de esas dependencias
## Este comando también se ejecuta en ese contenedor temporal
RUN pip install --no-cache-dir -r /tmp/requirements.txt


# Configuro mi ejecución

## Defino unas variables de entorno para mi contenedor
## ESTABLECIENDO UNAS VARIABLES DE ENTORNO EN NUESTRO CONTENEDOR TEMPORAL
## Pero, adicionalmete, estamos INFORMANDO a los futuros usuarios de la IMAGEN DE CONTENEDOR
## que vamos a generar, de que tengo esas variables de entornom, con esos valores... 
## que ellos podrían cambiar en un momento dado.
ENV RUTA_DATOS=/datos
ENV RUTA_DESTINO_MODELO=/exportacion

## Defino unos volumenes para mi contenedor
## ESTAS LINEAS SON PURAMENTE INFORMACIONALES:
## Aquí no creo volumenes... DE NUEVO SOLO:
## Informar a los futuros usuarios de la imagen de contenedor que vamos a generar
## de que podrán, si les interesa, montar unos volumenes en esas rutas...
## Que YO, HACEDOR DE LA IMAGEN, he considerado que son relevantes... y que uso en
## los programas que voy a instalar en esta imagen
VOLUME ["/datos"]
VOLUME ["/exportacion"]
VOLUME ["/codigo"]

## Establezco que cuando un comando sea ejecutado en este contenedor (TEMPORAL), 
## por defecto se ejecute en la carpeta /codigo
WORKDIR /codigo

## Una vez que docker lleva al final del fichero... y ha ido ejecutando / anotando todas esas cosas...
## Docker vuelca el contenedor temporal que se ha creado ... y sobre el que hemos ido trabajando
## a una imagen de contenedor... que luego podré utilizar para crear nuevos contenedores...
## Que ya tengan todo este trabajo realizado.

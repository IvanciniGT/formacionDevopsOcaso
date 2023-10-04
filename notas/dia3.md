# Objetivo: Servicio REST corriendo en Kubernetes/Openshift... configurado para un entorno productivo

Datos de entrenamiento irán evolucionando
    Preprocesamiento de los datos (está automatizado)
    Su propio proyecto -> Artefacto (DATOS... fichero... BBDD)

    En un momento dado, si hay nuevos datos -> Generar un modelo nuevo

Generación del Modelo
    Algoritmos... -> Modelo (Artefacto-pickle)

    Si hay un nuevo modelo -> Una nueva versión del servicio

Proyecto para el servicio REST que vamos a montar
    API ->  Swagger (1,2) -> OpenAPI(3)
        Para llamar a este servicio debes:
            Usar la URL: GET https://ocaso.es/api/v2/modelos/modeloA
                Parametros
                Cuerpo de la petición
    Implementación -> Artefacto
        Ese servicio expondrá un modelo predictivo
    En la formación no vamos a generar el API como proyecto independiente... pero en real sería la buena práctica

    Si hay una nueva versión del servicio -> Una nueva versión de la imagen de contenedor
        Si se incrementa el major del modelo, necesitaré cambiar código en el servicio

Necesitamos generar esa imagen de contenedor que contenga el servicio
    La generación de esta imagen la haremos mediante un Dockerfile... que 
    contendrá:
        - python (con las dependencias necesarias)
        - código de mi servicio
    Imagen -> Artefacto

    Una nueva imagen de contenedor, puede dar lugar a una nueva versión del chart
        Si se ha incrementado el major de la imagen de contenedor

Imagen de contenedor (al menos 1) -> Kubernetes 
    Lo hacemos a través de un CHART de HELM... que basicamente es una plantilla de despliegue
    La plantilla en si es un proyecto -> Artefacto (la propia plantilla de despliegue)

---

# Esquema de versionado:

VERSION: 1.2.3

                Cuando los incrementamos <- TAG en un repo de GIT
- Major 1       Breaking changes
                Hemos quitado algo de nuestro programa... que si alguien estaba utilizando... va jodido!
                    + nueva funcionalidad
                    + arreglos de bugs
- Minor 2       Nueva funcionalidad
                    + arreglos de bugs  
                Funcionalidad que se marca para su eliminación (obsoleta-deprecated)
- Patch 3       Cuando se arregla un bug (defecto) o varios

--- MOMENTO 1 DEL TIEMPO ------------------------------------------------------- DEVOPS CI(PRUEBAS)/CD

DATOS                                       1.0.0

MODELO                                      1.0.0
    DATOS v1.0.0
    texto -> [ [grupo, puntuación] ]
    Antes de usar ese modelo... dentro de un servicio, tendré que proibar que el modelo funciona
        -> poder de clasificación del modelo
        -> Si le llamo con unos datos, contesta?
        -> Si le llamo con datos incompletos, que me devuelva un error conocido!
        -> Pruebas de rendimiento > 4s UNITARIA
    
SERVICIO                                    1.0.0
    MODELO v1.0.0
    Antes de usar ese servicio... dentro de una imagen de contenedor, tendré que proibar que el servicio funciona
        -> Si le llamo por REST con unos datos, contesta?
        -> Si le llamo con datos incompletos, que me devuelva un error conocido!
        -> Prueba de RENDIMIENTO UNITARIA / Prueba de rendimiento de INTEGRACION

DOCKERFILE -> Imagen de contenedor          1.0.0
    SERVICIO v1.0.0
    Antes de usarla en un despliegue de Kubernetes , tendré que saber si funciona
        Tendré que crear una imagen... crear un contenedor con esa imagen... y llamarle al servicio... y ver que va bien si debe de ir bien
                                                                                                       y ver que va mal si debe de ir mal

CHAR HELM ->                                1.0.0
    IMAGEN v1.0.0
    Antes de usar el despliegue, lo tendré que probar en un entorno (cluster de Openshift) de pruebas
         y ver que va bien si debe de ir bien
         y ver que va mal si debe de ir mal
        -> Pruebas de rendimiento de SISTEMA -> ACEPTACION DEL CLIENTE
            (Y SI LA PRUEBA DA MAL?) En una petición me tarda 5 segundos en contestar = RUINA !
                No tengo NPI de donde esta el problema:
                    - En el despliegue de Kubernetes y la conf. que haya realizado (poca cpu al contenedor)
                    - Tengo un problema en el servicio
                    - Tengo un problema en el modelo
            

REQUISITO de rendimiento: 95% < 150ms
    
--- 2 MESES DESPUÉS ------------------------------------------------------------

CAMBIO LOS DATOS DE ENTRENAMIENTO
    Había datos mal catalogados                                                 v1.0.1
    Nuevos datos (más datos)                                                    v1.1.0
    Ahora hemos conseguido un campo adicional que pensamos que puede guardar    v2.0.0
        cierta relación con el campo objetivo de nuestra predicción:
            Nueva variable independiente
        Hay un cambio en la ESTRUCTURA del dataset? Breaking

                                            DATOS
MODELO será necesario regenerarlo
    Si solo había datos mal catalogados     -> 1.0.1                            v1.0.1
    Nuevos datos                            -> 1.1.0                            v1.1.0
    Nueva estructura                        -> 2.0.0                            v2.0.0          
    
El servicio si paso de v1.0.0 -> v1.1.0 No se ve afectado
Pero el servicio si paso de v1.0.0 -> v2.0.0 Si se ve afectado

---

Proyecto: MODELO de clasificación

# Vamos a definir el pipeline de Integración continua: JENKINS

Este pipeline, trabajaría sobre la rama RELEASE/DEVELOP

PASO 0: Partimos de un código Python que desarrollo ha depositado en un repo de GIT
PASO 1: Descargar ese código en un entorno independiente del entorno en el que trabajan los desarrolladores
PASO 2: Ejecutaré unas pruebas unitarias sobre él
PASO 3: Ejecutar un análisis de calidad de código (SONAR)
PASO 4: Generar un informe con el resultado de las pruebas unitarias < - UnitTest
PASO 5: Generar un informe con el resultado de las pruebas de calidad de código < - Sonar (Quality gate)
        - Recomendaciones del lenguaje: Acabar con una linea en blanco. 
                                        1 espacio en blanco delante y detras de operadores
                                        Utilizar snake-case para nombrar las variables
        - Complejidad cognitiva: Cómo de complejo es para un humano entender un código  ->
        - Complejidad ciclomática: Cuántos caminos puede tomar ese código al ejecutarse -> 
        - Duplicaciones de código
        - Vulnerabilidades
El propio pipeline acaba con estado: SUCCESS, FAILURE < - Jenkins
LISTO !

# Vamos a definir el pipeline de Entrega continua: JENKINS

(NOTA: Este pipeline, SOLO debería ejecutarse si el pipeline de Integración continua a acabado con éxito)
(NOTA2: Este pipeline SOLO debería de ejecutarse si en el REPO de git se ha etiquetado TAG un commit como release)
ESTE PIPELINE TRABAJARÍA SOBRE LA RAMA MASTER del repo

PASO 0: Tomar el código del proyecto de desarrollo
PASO 0.5: Llevar el código que hay en develop -> master
PASO 1: Ejecutar el proyecto -> modelo
PASO 2: Guardar ese modelo para que otros puedan usarlo (servicio rest) en un REPO de artefactos (ARTIFACTORY)
        Una alternativa es dejar ese artefacto en mi repo de git... y que otros proyectos (servicio) 
            usen ese repo de git como un submodulo

# Objetivo del pipeline

El objetivo es: Automatizar el proceso de PRUEBAS del modelo que estoy generando. Para que?
- Para tratar de identificar la mayor cantidad posible de FALLOS antes del paso a producción de este componente: VARIEDAD DE PRUEBAS
   Para asegurarme que el modelo no tiene fallos... FALACIA en el mundo del testing (ISTQB) -> Precisa la ejecución del programa: Pruebas dinámicas

    Al detectar un FALLO, que debo hacer? Arreglar DEFECTO
    Y para arreglar ese DEFECTO, lo primero que tengo que hacer es IDENTIFICARLO (Depuración, debugging)
    Y la prueba debe proveer información para la rápida identificación de un DEFECTO

- Para tratar de identificar la mayor cantidad posible de DEFECTOS.                         -> No preceisa la ejecución del programa: Pruebas estáticas
    -> Por ejemplo, las que hace el SonarQube 
        A sonar le da igual si el modelo predice bien o mal... no es su cometido.
        Le interesa que el programa guarde una determina estructura y pautas de creación.
        Si detecto un DEFECTO he de corregir ese DEFECTO

- La medida principal de progreso de un proyecto es: software funcionando
    Para saber cómo voy en un proyecto necesito un indicador. Vamos a usar el indicador SOFTWARE FUNCIONANDO

    Por qué se habla de ésto? Porque la forma en la que hemos estado midiendo el grado de avance (progreso) de un proiyecto ha sido tradicionalmente UN DESASTRE
        Cómo sabía el Jefe de proyecto qué tal iba el proyecto?
            MET TRADICIONALES: Planificación (Diagrama de gantt)... Lo que hacía yo era preguntar al equipo.. Qué tal vas? Los desarrolladores mentimos más que hablamos!
                               Número de lineas de código / datos procesados por semana
    Qué significa SOFTWARE FUNCIONANDO? Que el software funciona. Quién dice que el software funciona? LAS PRUEBAS !
        Cuántas pruebas se han superado esta semana de las que había que superar
    
    Requisito para ir a CI:    
    - Tener pruebas automatizadas -> Ganar tiempo cada vez que haya que hacer pruebas... si las voy a hacer muchas veces.
    CI -> Diariamente quiero un informe de pruebas del proyecto. Para que los desarrolladores puedan:
    - Ir corrigiendo los defectos / fallos que se van encontrando en el código... y no los arrastren en el tiempo
    - Que el equipo pueda conocer el estado del proyecto
    
    
    
    
---

Vocabulario en el mundo de las pruebas:
- ERROR     Los humanos cometemos ERRORES (por estar cansados, faltos de conocimiento, desconcentrados...)
- DEFECTO   al cometer un ERROR, introducimos un DEFECTO en un componente
- FALLO     que en un momento dado puede manifestarse como un FALLO

---

# Ejecutar mi app en un contenedor

Los contenedores los creamos desde imágenes de contenedor.
Hay 2 tipos de imágenes de contenedor:
- Tipo 1: Las que tienen ya un software listo para su uso
- Tipo 2: Las que me sirven de base para crear imagenes del tipo 1

## VOLUMEN

Es una ruta (carpeta o fichero) en el sistema de archivos (HDD) del contenedor
cuya persistencia real está fuera del contenedor

En el caso de docker, esa persistencia solemos tenerla en el sistema de archivos del HOST
En el caso de Kubernetes lo hacemos diferente:
    
    Cluster de Kubernetes                       Almacenamiento externo en RED
        Maquina 1 - OFFLINE
            contenedor con python
                datos   --------------------->  NFS, Volumen en Goggle Cloud AWS...
        Maquina 2                                   ^
            contenedor con python                   |
                datos   ----------------------------+


---

# En local, como desarrollador, puedo reemplazar los venv de python por un contenedor:

## Me creo un contenedor con la imagen de python que me interese (versión)
## Le comparto la carpeta de mi proyecto                                                        v Truco para conseguir que el contenedor quede en ejecución
docker container create --name mipython -v /home/ubuntu/environment/modelo:/modelo  python:3.12 sleep 3600  
                                                                                                cat
                                                                                                tail -f /dev/null

El comando docker realmente es un cliente que trabaja contra un servicio de docker. LO IDEAL ES ESTA... otra cosa es que te dejen!
El servicio de docker le puedo tener en mi máquina o en otra máquina

## Arranco el contenedor
docker container start mipython

## Le instalo cosas (dependencias)
docker exec -w /modelo mipython pip install pandas

## Voy ejecutando mi programa
docker exec -w /modelo mipython python modelo.py

---
# Jenkins

Formas de usar / instalar jenkins

    NODO MAESTRO    - Servidor (físico o virtual) con su SO... Jenkins.
     tiene instalado Jenkins
     
    NODOS TRABAJADORES - Servidor (físico o virtual) con su SO... Agente de Jenkins... + los requisitos de los procesos que vaya a ejecuatr este nodo.
                         Claro... puede ser que acabase con tropetantos nodos... para diferentes configuraciones de ejecución
                         Los etiquetaba: Modelos de Python | Aplicaciones JAVA WEB | ....

     En estos nodos es donde se ecjutan los pipelines

Cuando sale Jenkins esos NODOS Trabajadores los preinstalabamos y registrábamos en Jenkins

Hoy en día, en una instalación de Jenkins, los nodos trabajadores se generan bajo demanda... mediante un "CLOUD" (ojo, el concepto de Jenkins de cloud no es igual al concepto habitual que entendemos nosotros por cloud)
Un cloud de Jenkins, es un servicio que es capaz de proveerle de nodos trabajadores.
    - Docker
    - Kubernetes

Esta configuración la hago en Jenkins... pero es específica de cada proyecto!

Los logs de los contenedores son la salida estandar y de error del proceso que estas ejecutando.
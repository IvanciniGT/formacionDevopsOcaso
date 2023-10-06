


REPO datos 
    v1.0.0 master
    v1.1.0 master 
    v1.2.0 master 
    
REPO MODELO
    master v1.1.0 modelo < Dependencia con los datos < - v1.1.0
    develop v1.2.0 modelo... pendiente < v1.2.0 de los datos

REPO SERVICIO WEB
    master v1.1.0 servicio < Dependencia con el modelo v1.1.0
    hotfix v1.1.1 servicio < Dependencia con el modelo v1.1.0
        v
    master v1.1.1 servicio < Dependencia con el modelo v1.1.0
    
    
La version v1.1.0 del servicio está en producción
La versión v1.2.0 del modelo en desarrollo
Sale un bug en producción... y hay que arreglarlo...
Y resulta que el bug está en el servicio

---

REPO UNICO
    desarrollo
        datos       (v1.2.0)
        modelo      (v1.2.0)
        servicio    (v1.1.0)
    master
        datos       (v1.1.0)
        modelo      (v1.1.0)
        servicio    (v1.1.0)
    hotfix
        datos       (v1.1.0)
        modelo      (v1.1.0)
        servicio    (v1.1.1)        
        
    
---

App que empleados usan para registrar expedientes de un seguro de hogar
    - Se me rompió la vitrocerámica -> Electrodomésticos [x] -> manual -> Electricidad
    - Tengo un charco en el baño    -> Fontanería

DATOS -> REPO
    Ahora mismo solo tiene ficheros de datos
    Pero en un escenario real:
        - Ficheros de datos...
        - Datos sin procesar (ficheros, BBDD)
            -> Programas para transformar, limpiar, enriquecer... esos datos
            -> Quizás haya también trabajo manual (minimizarlo)
        - Datos procesados (ficheros... BBDD)
        - Exportar -> ficheros
    Si tuvieramos un proyecto más complejo, montamos también un Pipeline de Integración Continua:
        Que lance pruebas sobre los programas que he desarrollado, para ver cómo van y/o si están bien.
    Pipeline De Entrega Continua
        - Extraiga los datos finales... y los deje en un repositorio de artefactos (fichero)
        - Rama Desarrollo -> Rama master (En nuestro caso), con etiqueta
            SCRIPT CUTRE sh -> NECESITO QUE SE EJECUTE EN UN ENTORNO CON GIT
                git switch master
                git merge develop
                git push 
                git push --tags
            Y este script quiero que se ejecute cuando en desarrollo, un desarrollador pone a un commit
            una etiqueta con el formato: v#.#.# (puedo hacer algo más robusto... y asegurar que la versión que se está colocando es adecuada)
            
                v1.3.1
                    v1.3.0 ERROR
                    v1.3.2 o 1.4.0 o v2.0.0 SI

MODELO
    Pipeline en Jenkins: Actualizar datos
        Me pregunta: A que versión de los datos quieres IR? v.1.2.3
            -> actualizar_version_datos.sh v.1.2.3
        Forma de ejecución: MANUAL / AUTOMATICA? (Condicionada a que el PIPELINE DATOS CD haya ido bien)
    Pipeline CI: Probar el generador del modelo (PROGRAMA .py)
        Me pregunte: Quieres hacer pruebas de generación del modelo? (POR DEFECTO ES NO)
            QUE SI? 
                -> ejecutar_pruebas.sh  [DINAMICAS] - Depende (En nuestro caso es: GENERAR EL MODELO)
                -> Guarda el modelo que se ha generado -> Jenkins / Artifactory: modeloGuay v.1.1.0-RC4
            -> Mando el código a un SonarQube [ESTATICAS] - Cada día
        Forma de ejecución: Que se ejecute cada día a las 00:00 en AUTOMATICO
                            Manualmente cuando yo tengo todo listo (... o eso crea)
                            AUTOMATICAMENTE DESDE EL PROCESO DE CD
    Pipeline CD: Exporto ese modelo
        Primero: Ejecuta el de CI, con parametro SI generas el modelo
        Y si va bien:
            Guardar el arfacto (modelo) que genera el pipeline anterior en el artifactory / jenkins -> modeloGuay v.1.1.0
        Forma de ejecución: MANUAL
                            AUTOM. cuando en la rama desarrollo se genere un tag nuevo

Proyecto de DATOS
    git tag v1.2.3 && git push --tags : TODO SE HACE AUTOM.
Proyecto del MODELO
    git tag v1.2.3 && git push --tags : TODO SE HACE AUTOM.
    Y luego PLAY en Jenkins en la tarea CI / CD: Ahorro de tiempo, evito errores, y libero recursos
    
## ¿En qué entornos debe ejecutarse cada una de esas tareas que hemos metido en los pipelines?

Y la complejidad es alta... ya que cada TAREA DE CADA PIPELINE puede tener unos requisitos diferentes
    Pipeline CI del MODELO: Probar el generador del modelo (PROGRAMA .py)
            -> ejecutar_pruebas.sh: GENERA EL MODELO. 
                    Requisitos del entorno: PYTHON 3.12 + librerías de python + GPU
            -> Mando el código a un SonarQube [ESTATICAS] - Cada día
                    Un entorno con el agente de SonarQube (SonarScanner)

Nosotros definiríamos 1 POD, con 2 contenedores:
    - Contenedor 1: 
        Imagen: sonarsource/sonar-scanner-cli
    - Contenedor 2:
        Imagen: python con mis requerimientos (dockerfile)

Además, JENKINS en automático añadirá un tercer contenedor... yo ni me entero: Agente de Jenkins,
    para posibilitar la comunicación entre mi pod y Jenkins

Y Jenkins montará un volumen no persistente, compartido entre esos contenedores, de forma que yo vaya dejando ficheros en uno y el otro los pueda leer.
Por ejemplo... el código

Para ello es para lo que tiramos de CONTENEDORES... 
    pero... en entornos de producción, esos contenedores los gestionamos mediante Kubernetes 
    Donde la unidad de trabajo es un POD
        POD: Un conjunto de contenedores que:
             - Se despliegan en el mismo host
             - Escalan juntos
             - Comparten configuración de red... y por ende IP... y además pueden usar para copmunicarse entre si la palabra LOCALHOST
                                             comparten la red de loopback.. y la IP: 127.0.0.1
             - Pueden compartir volumenes de almacenamiento... de forma que pueden compartir archivos entre si
    En Kubernetes todo el trabajo se gestiona mediante PODs... 
        - Un pod tendrá al menos 1 contenedor
    Desde Jenkins diré... QUIERO TENER UN POD, donde se ejecuten los trabajos de este PIPELINE
    Y ese pod tendrá varios CONTENEDORES... o 1, si es sencillo PIPELINE que vaya a ejecutar.
    Para cada POD defino:
        - Sus contenedores:
            - Imagen
            - Comando
            - Sus variables de entorno
            - ...
        - Los volumenes: 
            De cada volumen, dire su tipo:
                - PERSISTENTES    * En algún caso
                - NO PERSISTENTES * SIEMPRE

Para que sirven los volúmenes cuando trabajo con contenedores?
    - Persistencia (BBDD, ELASTICSEARCH, KAFKA)
    - NO QUIERO PERSISTENCIA: 
        - Inyectar información (archivos, directorios)
        - Compartir informacion entre contenedores
         emptyDir
         hostPath


La página web de amazon
                                ETL: 
                                E: Estraer de los servidores
                                T: Enriquecer los datos: IP -> GEO POSICIONAMIENTO
                                L: Cargar al elastic

Maquina 1:  
    POD1: El pod me puede perder conectividad (Eso significa que tampoco recibe nuevas peticiones.)
        - Servidor web: CONTENEDOR 1
                v
            - Logs accesos  VOLUMEN PERSISTENTE?                                 T -> L
                ^               depende de lo crítico que sea el dato
                ^                   MUY CRITICO... HIPERCRITICO: Volumen de almacenamiento independiente
                ^                                                   Prepara BILLETON !!! Almacenamiento
                ^                                                                        Desarrollo, para la gestión de esos volumenes
                ^                                                                        RED (la colapso)
                ^                                                                        Tiempos de respuesta
        - FileBeat | Fluentd: CONTENEDOR 2
            Cada linea que se escriba, la mandan al KAFKA
            
        - Lo que montamos es un volumen no persistente con almacenamieto en RAM
            Donde dejo 2 ficheros rotados de un tamaño preestablecido: 100Kb <<<
            Y en ellos se escribe y de ellos se lee
            Si pierdo conectividad con KAFKA... en cuanto de la vuelta el fichero... pierdo el dato
            
    POD2:                                KAFKA  --->     Logstash       --->     ELASTICSEARCH   < - Kibana
        - Servidor web                  Esto no se cae
        - Logs accesos
Maquina 2:
    PODn:
        - Servidor web
        - Logs accesos
Maquina M:
    PODm:
        - Servidor web
        - Logs accesos
    
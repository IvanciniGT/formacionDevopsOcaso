# La gran diferencia entre contenedores y máquinas virtuales


## Forma tradicional de INSTALAR software
    
        App1 + App2 + App3              Trabajar así es IMPENSABLE en un entorno de producción
    ------------------------            Dios no lo quiera... y seguro que no ocurrirá nunca ( ya que los programas son PERFECTOS por definición)
              SO                            Que App1 tenga un bug, se vuelva loca y ponga la CPU para freir huevos (100%) -> App1 se vuelve inaccesible NO CONTESTA
    ------------------------                + App2 y App3 ---> Offline
            HIERRO                      Otros problemas: Incompatibilidades de dependencias, configuraciones...
                                                         Seguridad: Potencialmente APP1 puede acceder a los ficheros de App2.. o incluso a zonas de memoria RAM (VIRUS)

## Máquinas virtuales

    ------------------------
       app1  | app2 | app3              Me permiten asilar los entornos de ejecución de cada proceso:
    ------------------------                Cada MV tiene su propia IP
       SO 1  | SO 2 | SO 3                                su propio Sistema de archivos (HDD)
    ------------------------                              sus propias variables de entorno
       MV 1  | MV 2 | MV 3                                y limitación de acceso a los recursos de Hierro
    ------------------------
        Hipervisor: VMWAARE,            Pero... esto ha venido con sus propios problemas:
        CITRIX, HYPERV                  - Merma de recursos: 4 SOs en funcionamiento... usando RAM ... CPUS de procesos en segundo plano...HDD que ocupan un montón
        VirtualBox, KVM                 - Merma en el rendimiento
    ------------------------            - Folón de instalaciones y mnto.
              SO
    ------------------------
            HIERRO

## Contenedores

    ------------------------
       app1  | app2 | app3              Esto me resuelve los problemas de las instalaciones a hierro... igual que operar con máquinas virtuales
    ------------------------            PERO SIN NINGUNO de los problemas de las MV
       C  1  | C 2 |  C  3               Y encima siguiendo un estandar
    ------------------------                - Las imágenes de contenedor siguen un ESTANDAR: De forma que pueden ser ejecutadas por cualquier gestor de contenedores
     Gestor de contenedors                  - Estandarizan la forma de operar esos contenedores: ARRANCA, PARA, LOGS; REINICIA
     Docker, podman, crio...
    ------------------------            Ya no más Máquinas virtuales (o casi... para usos muy específicos)... Los entornos de prod ahora van con contenedores
            SO (Linux)                  Pero no solo esos... yo en mi máquina, si tengo que ti stalar algo: PYTHON, MYSQL, ... -> Contenedor
    ------------------------                No tiene ya sentido instalar cosas a hierro en ningún entorno.
            HIERRO
                                        Y encima al trabajar con contenedores me evito instalar oftware (solo despliego... descomprimo)
                                        
                                        
Los contenedores a diferencia de las Máquinas virtuales NO EJECUTAN UN SISTEMA OPERATIVO... de hecho ESTO NO SE PUEDE HACER CON CONTENEDORES
No puedo crear un contenedor que tenga dentro un Sistema Operativo. Por definición!
                                        
# Contenedor

Un entorno aislado dentro de una máquina con SO Linux (SO que esté ejecutando un kernel linux) en el que ejecutar procesoS.

Entorno aislado:
- Su propia configuración de RED -> Su propia IP
- Su propio Sistema de Archivos (HDD y carpetas)
- Sus propias variables de entorno
- Puede tener limitación de acceso a los recursos del HW (hierro).

Los contenedores los creamos desde IMAGENES DE CONTENEDOR

Una cosa que nos dan los contenedores es una ESTANDARIZACION sobre la forma DE OPERAR un programa:
    docker start 
    docker stop
    docker restart
    docker log

# Imagen de contenedor

Es un triste fichero comprimido (tar), que usualmente contiene carpetas comprimidas con estructura POSIX.
Dentro de esas carpetas encontramos programas YA INSTALADOS de antemano, con sus:
- configuraciones
- dependencias
Y además, suelen venir otros programas preinstalados en esas carpetas... que me puedan ser de utilidad en un momento dado.

Las imágenes de contenedor las descargamos de registros de repositorios de imágenes de contenedor:
- Docker hub
- Quay.io       (REDHAT)
- Las empresas suelen montar sus propios registros (Artifactory)

# POSIX

Es un estandar, acerca de cómo montar un SO. En ese estandar, que siguen los SO UNIX® y también Linux, se definen una serie de carpetas:
/bin        Comandos ejecutables (cp, mv, ls...)
/etc        Configuraciones de programas
/opt        Programas
/var        Datos de programas (Ficheros de una BBDD, logs)
/tmp        Archivos temporales. Al reiniciar el sistema, se borra autom.
/home       Carpeta del usuario

# Instalar MySQL en mi máquina Windows

PASO 0: Garantizar que tengo instaladas las dependencias necesarias para ese programa (librerías...)
        Este también puede requerir de instalar muchas cosas
PASO 1: Descargar de internet un instalador del programa
PASO 2: Ejecuto el instalador, para dar lugar a una INSTALACION del MySQL
            c:\Archivos de programa\MySQL -> ZIP y os lo mando via email < Esto es una imagen de contenedor
        Este paso puede ser complejo. Hay programas cuya instalación es Siguiente... siguiente....
        Pero otras veces, es necesario configurar un montón de cosas... que exigen conocimiento propio del programa
PASO 3: A disfrutar
        

# Los contenedores se operan desde GESTORES DE CONTENEDORES:

- Docker
    Sintaxis declarativa para crear contenedores con Docker
- Podman
- ContainerD
- CRIO

Estos operan contenedores a nivel de 1 máquina (no vale para entornos de producción per se)
Los gestores de contenedores tienen configurados unos registros de repos de imagenes de contenedor por defecto:
    Docker -> docker hub
    Podman -> quay.io -> docker hub

# Gestores de Gestores de contenedores

- Swarm         <<< Esto es un intento de producto de la gente de Docker para Entornos de producción (RUINA)
- Kubernetes
    - K8s
    - K3s
    - Openshift
    - Tanzu
    ...
    
Me permiten usar contenedores en entornos de producción (CLUSTERS)

# Entorno de producción:

Qué características tiene un entorno de producción que le diferencia del resto de entornos?
- Alta disponibilidad: Tratar de garantizar que los programas estén en funcionamiento un determinado porcentaje 
                       del tiempo que deberían estar en funcionamiento.
                       Tratar de garantizar la NO PERDIDA DE INFORMACION ! que es el activo más valioso que tiene una empresa!
                            En un entorno de prod el estandar es que cada dato al menos se guarde en 3 sitios diferentes!
                       Es la carta a los reyes magos!!!!!
                       
    Quiero que este modelo (me gustaría... ojala) esté funcionando el 99% del tiempo que debería (9-14 de L-V)
    Esto se consigue mediante replicación.
    
    Programa A                  90% del tiempo que debería (GARANTIZAME) RUINA -> 1 de cada 10 dias el sistema offline. 36,5 días al año    | €
    Programa B                  99% del tiempo que debería                     -> 3,5 días al año puede estar offline                       | €€
        Web de una peluquería de barrio. Manolo!                                                                                            |
            Instalar aquello en el pc gamer de su hijo                                                                                      |
    Programa C                  99.9%                                          -> 8 horas /año                                              | €€€€
        Monto 2 servidores iguales CLUSTER                                                                                                  |
    Programa D                  99.99%                                         -> 20 minutos al año                                         | €€€€€€€€€€€€€€€
        Monto 2 servidores iguales en 2 zonas geografías diferentes, con 2 proveedores de internete. generadores electricos..               v 

Las máquinas tienen defectos... los programas tienen defectos... se me puede joder un HDD, una fuente de alimentación,
haber un incendio, perder internet, corte de luz, terremoto...

- Escalabilidad
    Capacidad de ajustar los recursos (infraestructura) a las necesidades de cada momento.
    
    App1: De un departamento. Hospital (citas). Esto existe... aunque cada vez menos... pero sigue existiendo
        Dia 1:          100 usuarios
        Dia 100:        102 usuarios            NO NECESITO ESCALABILIDAD
        Dia 1000:        98 usuarios
    
    App2: Cada vez tengo más usuarios 
        Dia 1:          100 usuarios
        Dia 100:       1000 usuarios            ESCALABILIDAD VERTICAL: MAS MAQUINA !
        Dia 1000:     10000 usuarios

    App3: Esto es lo mún hoy en día (INTERNET)
        Hora n:      100 usuarios
        Hora n+1:    1000000 usuarios
        Hora n+2     20000 usuarios
        Hora n+3:    2000000 usaurios

        Web del telepi: 02am -> 0 usuarios
                        08      0
                        12      5
                        14      500             ESCALABILIDAD HORIZONTAL: MAS MAQUINAS ! ---> CLOUD !
                        17      10  
                        21      Madrid/Barça... agarra que nos vamos !!!!
                        00      0 
                        
Estas características me impoenen trabajar con clusters!

KUBERNETES: < Quiero 3 instalaciones de mi web
    Maquina 1
        CRIO / ContainerD
            Servidor web    ---IP1--+
    Maquina 2 --> OFFLINE           |
        CRIO / ContainerD           |
    Maquina 3                       |
        CRIO / ContainerD           |
            Servidor web    ---IP2--+----Balanceador de Carga------Proxy reverso ----------  Usuario
    Maquina N                       |         (servicio)            (proteger)
        CRIO / ContainerD           |                               (ingress-controller)
            Servidor web    ---IP3--+


 ------------------- Red de mi empresa ---------------- MenchuPC
  |
  172.31.46.205:8080 -> minginx:80
  |
  Servidor en Amazon
  |     |- 172.17.0.2 minginx
  |     |- 172.17.0.3 minginx2
  |     |
  |     | docker
  |       172.17.0.1
  | loopback
    127.0.0.1
    
    
# Linux

Linux no es un SO.
Linux es un Kernel de SO

Todo SO tiene su kernel... Windows incluido
- Microsoft a lo largo de sus historia ha creado 2 kernels , que ha usado para sus innumerables SO
    - DOS -> MS-DOS..., Windows 2, Windows 3, Windows 95, Windows 98, Windows millenium
    - NT  -> Windows NT, Windows XP, Windonws 7, 8, 10, 11 , Windows Server
    
Hay pocos SO con kernel Linux
- GNU/Linux Esto es un SO... al que posteriormente se le ponen otros programitas por encima para dar lugar a distros de GNU/Linux
  70% 30%
            - Redhat Enterprise Linux < Fedora
            - Debian > Ubuntu > Ubuntumint, Xubuntu
            - Suse
            - ...
- Android (Es un SO que corre dentro el kernel de Linux)

Y entonces en Windows no puedo ejecutar contenedores? SI... pero windows no tiene el kernel NT? SI
                                                      Pero desde hace unas cuantas versiones de Windows, 
                                                      podemos ejecutar en paralelo con el kernel NT un kernel Linux dentro de Windows: WLS
                                                      

---

Modelo dado un texto (Incidencia) -> Clasificarlo (Fontanería, Albañilería....)
    Python

función en python -> texto -> lista de grupos con puntuaciones
    MODELO
    
Cómo expongo ese modelo al mundo

App web corporativa-> texto -> listado de grupos ordenado <- 

Servicio REST python flask

---> Cuantas partes tiene este proyecto? 
Generar el Modelo (programa que ofrece opciones de clasificación)
    Datos que hay que preparar
    Entrenarlo -> Parametrización -> 
Exponer el modelo, mediante un Servicio REST


---> Cuantos repos de git creo para esto? 
    2 repositorios: Código del modelo
                    Expocision del modelo mediante REST

Hoy en día, hemos aprendido a que los sistemas MONOLITICOS son una ruina de mantener!
Y vamos a otro tipo de arquitecturas
- Arquitecturas componentes independientes que se comunicacn entre si... mediante APIs limpias. CON BAJO NIVEL DE ACOPLAMIENTO
    - Arquitecturas orientadas a microservicios
    
Principio SOLID de desarrollo de software -> Los recopila El tio BOB
S-> Single Responsability: Responsabilidad única: 
    Un compoente debe tener una única razón para cambiar.
    
Modelo: Función PY (texto) -> Clasficiaciones puntuadas 
Otra cosa es cómo expongo ese modelo: API REST v1
                                      API SOAP v1
                                      API REST v2
REPO modelo que lleva su sistema de verisonado
REPO exposicion del servicio que lleva su versionado independientes
REPO con el servicio 
    -> REPO modulo
    -> REPO exposicion SUBMODULOS DE GIT 
Imágen de contenedor < ENTREGABLE > REPO DE ARTEFACTOS (RELEASE)
    Ésta imagen no es algo que me deberían de generar... en la imagen YO, creador del sfotware soy el que conozco que dependencias tiene mi aplicacitovo
    y por ende, el que puedo configurar la imagen.
REPO con la generación de la imagen de contenedor -> Dockerfile
REPO de git
Al final ésto acaba desplegado en un cluster de kubernetes:
    Plantilla de despliegue en Kubernetes -> REPO DE ARTEFACTOS -> HELM (chart)
    
Jenkins con los procesos de CI / CD / CD


MODELO -> Pipeline1: CI Probar que el modelo funciona correctamente
                    Le pasaremos unos datos de prueba... y a ver si los clasifica bien.
          Pipeline2: CDelivery: Dejo el modelo en un repo de artefactos
          v^
EXPOSICION MEDIANTE FLASK -> Pipeline3 de CI Preuba de que puedo llamar a ese servicio con el API REST Definido y que contesta adecuadamente
                             Pipeline4 de CDelivery: Dejar el servicio en un repo de artefactos
Generación de la imagen de contenedor:  Pipeline5 de CI: Prueba de que el contenedor se genera adecuadamente
                                        Pipeline6 de CDelivery: Genero una imagen de contenedor que dejo en un repo de artefactos
Generación de un chart de HELM (una plantilla de despliegue en Kubernetes): Pipeline7 CI: Para ver que se realiza bien un despliegue en un entorno de pruebas
                                                                            Pipeline8 de CDelivery: Para dejar la plantilla en un repo de artefactos
                                                                            Pipeline9 de CDeployment: Se haga la instalación en producción
Eso sería devops
Recopilar datos del entorno de producción que ayuden a mejorar el modelo... y cierro el circulo!

Tendremos pipelines adicionales de Jenkins que podemos crear:
- Quiero un pipeline que cuando alguien haga un commit etiquetado en la rama mastaer del modelo:
    -> pipeline 1                       +Incrementa mi confianza
        -> pipeline2
            -> pipeline 5               +Incrementa mi confianza
                -> pipeline 6
                    -> pipeline 7       +Incrementa mi confianza
                        -> pipeline 8
                            -> pipeline 9 < CONFIANZA
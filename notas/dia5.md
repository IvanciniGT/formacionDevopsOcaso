                  +------------------credencial-------------------------------------+
                  |                                                                 |
                  v                                                                 |
    pipeline < JENKINS > Kubernetes                                                 |
                  |         v                                                       |
                  +------> Pod                                                      |
                            - contenedor: sonar-scanner ----- credenciales --->  SonarQube

## Kubernetes

Gestor de gestores de contenedores para automatizar la operación de un entorno de producción

### POD

Es un conjunto de contenedores que:
- Comparten configuración de RED (se hablan entre sí a través de la red de loopback: localhost)
- Se despliegan juntos en el mismo host
- Pueden compartir volumenes
- Escalan juntos


Quiero montar una página WEB: 
    servidor web  - Contenedor 1
    base de datos - Contenedor 2
    
Esos 2 contenedores los pondría en un único pod o cada uno en un pod dentro de Kubernetes:
Siempre irían en distintos PODs
- No quiero que escalen juntos
    En un momento dado puedo tener la necesidad de 3 servidores WEB trabajando en paralelo (tengo muchas peticiones)
    Pero quizás con un único servidor de BBDD me es suficiente para satisfacer la demanda de los 3 servidores web
    De hecho, nunca querría tener una bbdd para cada servidor web... Me meto en un problema de sincronización de datos.

# YAML

Servicios los meteis en YAML
Kubernetes|Openshift: YAML
Docker compose: YAML
Linux: Configuración de red
Gitlab CI/CD: YAML

---

# Kubernetes es una herramienta orientada a entornos de producción

Y por ende, debemos dar toda la configuración propia de un entorno de producción.
Habitualmente usamos Kubernetes para desplegar y operar aplicativos en entornos con HA.

Servicio WEB REST para exponer la funcionalidad de un modelo

    GET https://ocaso.es/api/v2/modelo ---> llamada a una función Python, pasándole como argumentos: (BODY:texto)
        BODY: texto

        Response:
            BODY:
            {
                "classification": {
                    "info": {
                        "count": 2,
                        "max_score": 5
                    }
                    "tokens": [
                        {"token": "fontanería", "score": 5},
                        {"token": "carpintería", "score": 3}
                    ]
            }    

Eso es un programa... otra cosa es lo que necesito en un entorno de producción para que eso funcione.
Al trabajar con una herramienta como Kubernetes, por debajo estamos trabajando con contenedores:

    Imagen de contenedor:
        Que tenga dentro: NUESTRO SERVICIO REST
        Y además, python, flask... las dependencias que nuestro servicio REST necesita para funcionar

    Necesito contenedores creados desde esa imagen para hacer el trabajo (atender peticiones)
    Esos contenedores se depliegan en los servidores de nuestro cluster de Kubernetes.
    Pero... ya hemos dicho que en Kubernetes lo que trabajamos es con PODs y no con contenedores.
    Ya habeis visto como definir un POD.
    Al POD le puedo dar una limitación de recursos: CPU, RAM... eso lo hago siempre:
    POD: NUESTRO SERVICIO WEB REST: 4 cores + 16Gbs de RAM
    Un trabajo que debo hacer es estimar con esa limitación de recursos, cúantas peticiones puedo atender por unidad de tiempo:
        100 peticiones/minuto <- Mediante pruebas de rendimiento soy capaz de estimar
    
    
    El problema es que yo no quiero tener un POD dentro de mi cluster.
        Y si estoy recibiendo 150 peticiones/minuto... qué pasa? Mi pod no da de si. Necesito otro pod igual que este nuevo.
            -> Querré tener un número variable de ellos... 
               Voy a estar creando yo esos pods? NO... quiero automatizar ese trabajo.. y que lo realice: KUBERNETES !
        Y si tengo 30 peticiones/minuto, con 1 pod me sirve? SI
        Pero.. qué pasa si el pod está en un servidor que se rompe!
            -> Querré que Kubernetes cree un POD igual que el anterior en otra máquina
        Y si tengo un pod... que deja de responder? 
            -> Querré que Kubernetes lo mate, lo borre ... y cree otro pod <<<<<

Si yo creo un POD en Kubernetes... y el pod se muere... pues muerto se queda
Si yo creo un POD en Kubernetes .,.. y en un momento no es capaz de atender suficientes peticiones... pues mala suerte!

Y por ello, yo no quiero crear PODs en Kubernetes... 
sino PLANTILLAS DE PODS cuando necesite desplegar una aplicación lista para producción: HA y ESCALABILIDAD

    apiVersion: v1
    kind: Pod
    metadata:
        name: pod-servicio-rest-modeloA
    spec:
      containers:
      - name: servicio-rest-modeloA
        image: servicio-rest-modeloA:v1.2.3
    
    vvv

    # Plantilla de pod
    apiVersion: v1
    kind: Deployment # Statefulset, DaemonSet
    metadata:
        name: plantilla-servicio-rest-modeloA
    spec:
      replicas: 2 # Número inicial de replicas
      template:
          containers:
          - name: servicio-rest-modeloA
            image: servicio-rest-modeloA:v1.2.3
    ---
    kind: HorizontalPodAutoscaler
    ...
    spec:
        ... # Quiero entre 2 y 10 replicas
        # En base al uso de CPU y de RAM: Si la media de uso de CPU o RAM de los pods supera un 50%, escala
    ---
    kind: Service # Balanceador de carga
    ---
    king: Ingress # Regla para un proxy reverso... Que en definitiva me asigna un nombre público para acceder al modelo:
        https:/ocaso.com/api/v1/modelo -> BALANCEADOR -> PODs -> Contenedores -> Programa python
        
---

Tenemos un programa que corre en un contenedor

    docker image pull nginx:latest
    docker container create --name minginx nginx:latest
    docker container start minginx

    docker run --rm --name minginx -d nginx:latest

Dentro de un contonedor ejecuto tantos procesos como quiera... pero:
EL PROCESO con el que se inicia (start) un contenedor, es el proceso que Docker monitoriza
Si ese proceso muere o acaba, para docker el contenedor ha terminado.. aunque tenga otros procesos en ejecución

Ese control es el más básico que podemos hacer sobre un contenedor... y lo hace tanto docker como Kubernetes

Pero eso, en un entorno de producción NO ES SUFICIENTE !

Imaginad que monto un servicio REST para exponer un modelo de clasificación
EVIDENTEMENTE... si ese servicio (proceso) corre en un contenedor... y el proceso explota (acaba)
quiero que se entienda (kubernetes, docker...) que el contenedor ha fallado.... y en un entorno de producción
me gustaría que rápidamente docker (kubernetes) levantase otro!
PERO NO BASTA !
Podría ser que el proceso siga corriendo (en funcionamiento)... pero que no esté respondiendo a las peticiones:
- Cola de peticiones llena!
- Esta ejecutando un trabajo que le está llevando mucho tiempo... y consume todos los recursos... y no hay hueco para ejecutar nuevos trabajos
- Otros bugs: DeadLock: Un hilo ejecutando un trabajo... y a la espera de respuesta de otro hilo que estaba ejecutando otro trabajo...
  pero que también estaba a la espera de una información del primero
   HILO A ---> Esperando ---> HILO B
   HILO B ---> Esperando ---> HILO A  DEADLOCK

En docker, al crear un contenedor se le puede espeficicar un HEALTH_CHECK
Básicamente es una prueba de que el contenedor está en un estado saludable!
Docker, cada 5 segundos ejecuta: GET http://localhost/api/v1/modeloA?texto=bañera -> fontanería en menos de 2 segundos
        Si... esto falla 3 veces consecutivas que lo ejecutes... considera que el contenedor NO ESTA SALUDABLE !
        
En Kubernetes hay algo parecido.... pero a lo bestia.
Y es algo que los desarrolladores deben tener en cuenta a la hora de montar sus aplicativos.

En Kubernetes, un POD puede estar en varios estados:
- INITIALIZING: Cuando un contenedor se crea y arranca, en autom. pasa a estado: INITIALIZING
    ---> StartupProbe. 
        Eso es una prueba... que hago sobre el contenedor... 
            Hacer una llamada por http a una ruta del contenedor
            Ejecutar un comando dentro del contenedor
        Si la prueba se supera, el contenedor se marca como INITIALIZED
        Si la prueba no se supera un determinado número de veces, que especificamos, el contenedor se marca como FALLIDO
- INITIALIZED
    ---> Liveness Probe.
        Eso es una prueba... que hago sobre el contenedor... 
            Hacer una llamada por http a una ruta del contenedor
            Ejecutar un comando dentro del contenedor
        Si la prueba se supera, el contenedor sigue en estado INITIALIZED
        Si la prueba no se supera un determinado número de veces, que especificamos, el contenedor se marca como FALLIDO
    ---> Readyness Probe.
        Eso es una prueba... que hago sobre el contenedor... 
            Hacer una llamada por http a una ruta del contenedor
            Ejecutar un comando dentro del contenedor
        Si la prueba se supera, el contenedor pasa a estado READY.. 
            y podrá ser usado en el balanceador
        Si la prueba no se supera un determinado número de veces, que especificamos, el contenedor se marca como INITIALIZED
- READY
    ---> Readyness Probe.
        Eso es una prueba... que hago sobre el contenedor... 
            Hacer una llamada por http a una ruta del contenedor
            Ejecutar un comando dentro del contenedor
        Si la prueba se supera, el contenedor pasa a estado READY.. y esto tiene su implicación
        Si la prueba no se supera un determinado número de veces, que especificamos, el contenedor se marca como INITIALIZED
- FALLIDO
    Si un contenedor está FALLIDO, en AUTOMÁTICO el pod que contiene el contenedor es destruido
    y uno nuevo es creado en su lugar.

Cómo un contenedor llega a estado FALLIDO? 
- Si el proceso principal que ejecuta se muere! NO ES SUFICIENTE

---

Pod 1 -- Servicio REST modeloClasificacion      <<<
    TIPO: pod-con-modelo-clasificacion
Pod 2 -- Servicio REST modeloClasificacion      <<<      Balanceador de Carga    <<<     Cliente final
    TIPO: pod-con-modelo-clasificacion
Pod 3 -- Servicio REST modeloClasificacion      <<<
    TIPO: pod-con-modelo-clasificacion

Cliente final: APP WEB
    https://ocaso.es/api/v1/modeloClasificacion
        ocaso.es    ->  Proxy reverso (IngressController)
                                https://ocaso.es/api/v1/modeloClasificacion ->  https://balanceador/api/v1/modeloClasificacion
                                                                                        |
                                                                                        v
                                                                                https://pod1/api/v1/modeloClasificacion
                                                                                
La configuración del balanceador la gestiona Kubernetes internamente.
Aunque alguien debe crearla... Alguien dirá...
    Cuando se haga una peticion al balanceador, el balanceador debe redirigir esa petición
    a un pod que haya de un determinado TIPO: pod-con-modelo-clasificacion -> CREAR UN SERVICIO en Kubernetes
                                                                                
Kubernetes monitoriza en cada momento los pods que hay de ese tipo, que estan READY para prestar el servicio.
Y los añade al balanceador para que empiecen a recibir peticiones.
Si un pod de ese tipo no está READY o deja de estarlo, es eliminado del balanceador.

---

Para qué sirve esto:

BBDD
Arrancará... y tardará X tiempo en arrancar... y una vez que arranque pasará a estado ARRANCADA (INITIALIZED)

Pero una vez arrancada (VIVA)... quizás no siempre está lista para prestar servicio
- Por ejemplo: Si la BBDD la pongo en modo administarción para hacerle un backup... la BBDD está ARRANCADA... y viva
               PEro en ese momento no es capaz de atender petición alguna por parte de mis usuarios.
  Eso significa que debo matarla? NI DE COÑA... está haciendo sus trabajos... está bien... dejala.... ya acabará!
  Pero no la quiero dentro del balanceador, ercibiendo peticiones de mis usuarios.
  
 
---

Servicio REST para exponer un modelo de Clasificacion
    STARTUP
        http://localhost/api/v1/status -> OK (el servidor ha arrancado)
            Si eso no llega a contestar, es que el servicio no arrancó bien.... y quiero un nuevo pod
    LIVENESS
        v
        http://localhost/api/v1/modelo?texto=bañera -> fontanería
            Si esto contesta, el pod debe entrar a formar parte del balanceador (READINESS)
            Si esto no contesta, el pod debe ser eliminado y generarse uno nuevo (LIFENESS)
        ^
    READINESS

Estas pruebas son medidas de gracia que os da Kubernetes... teniendo en cuenta que el software SEGURO que presenta defectos.. que no he cazado en PRUEBAS
    En paralelo, debería intentar averiguar cuál es el DEFECTO que hace que el contenedor haya quedado sin responder...
    ... pero entre tanto, Estas pruebas me aseguran que sigo dando servicio a mis clientes!

ESTO IMPACTA EN DESARROLLO... he de definir esos endpoints
Esas rutas las he de montar yo en desarrollo... en mi servicio
Y se las paso al equipo que despliega mi app en kubernetes, para que ellos las configuren en el despliegue

ESTO Es lo que aporta un Kubernetes... frente a una herramienta como Docker... que NO ESTA PENSADA PARA ENTORNOS DE PRODUCCION


## Limitar el acceso a recursos de HW
resources:
    requests:       El mínimo que debe ser garantizado a mi app para atender un número X de peticiones/unidad de tiempo
        cpu:    2
        memory: 4Gi
    limits:
        cpu:    4      # Todo lo que pueda... no tiene mucho impacto
        memory: 4Gi    # Va siempre igual al de arriba. Solo si tengo un coniocimiento muy profundo de la app... y de mi entorno... en algunos casos puede tener sentido cambiarlo

4Gi -> 4 Gibibytes... Mebibytes... Kibibytes
4Gb -> 4 x 1000 Mb... antes era 4 x 1024 Mb
Lo que antes era 4Gb... ahora son 4Gi = 4 x 1024 Mib

---

DATOS
    CIntegracion -> Programas que extraen / transforman los datos > Informe de pruebas
    CDelivery -> Copiar los datos de la rama desarrollo a la rama master
    
MODELO
    submodulo de GIT: DATOS
    CIntegracion -> Informe de pruebas
    CDelivery    -> Copiar el commit de la rama develop -> master
                    Ejecutar la generación del modelo (ejecutar.sh --export)
                    El modelo que se genera se sube a un artifactory

SERVICIO REST
    requirements.txt
        Dar de alta el artefacto que hemos subido en el CD del proyecto MODELO con la versión correspondiente
    CIntegration -> Informe de pruebas (Sonarqube)
    CDelivery    -> Aquí genero un artefacto que subo también a Artifactory
                    Artefacto? Imagen de contenedor que lleve dentro el servicio ya INSTALADO
    CIntegration2 -> Usar el chart de helm para hacer un despliegue en el cluster de test
                     Donde haga unas pruebas que me demuestren/confirme que el servicio se despliega correctamente
                        Aquí hago el despliegue con unos parámetros más básicos (memoria/cpu...)
    CDeployment   -> Usar el chart de helm para hacer un despliegue en el cluster de producción
                        Aquí hago el despliegue con los parámetros más de prod (memoria/cpu...)

Despliegue en Kubernetes
    Mi app... que tendré que crear un megafichero YAML... con:
        - Plantillas de Pods            Deployments | Statefulsets
            - Pruebas
            - Requisitos de HW (cpu, memory)
        - Balanceadores                 Services
        - Configuraciones               Configmaps | Secrets
        - Rutas para acceder a mi app   Ingress
        - Autoescaladores               HorizontalPodAutoscaler
            Quiero tener entre 2 y 20 pods...
    la desplegaré en un solo entorno... o en varios entornos de Kubernetes?
        Llamarme loco... al menos en 2: TEST & PROD
    Y en esos entornos... la configuración del despliegue será la misma? NO es la misma.
        En TEST memos memoria, menos CPU, Volumenes de almacenamiento ECONOMICOS... un escalado inferior 2...3 (lo justito para hacer una prueba y ver que el escalado funciona!)
    Y que voy a tener? 2 megaficheros con distintos parametros?  NO TIENE SENTIDO... SERIA MUY COSTOSO DE MANTENER y propicio a errores humano
    
    Y lo que hacemos aquí es generar UNA PLANTILLA DE DESPLIEGUE: CHART DE HELM
    
    CI: Pruebas de un despliegue
    CDelivery: Deje en artifactory / Git mi chart de helm
    
---
    
La adopción de una cosa como esta es MUY LENTA en una empresa !

Generación de modelos... Cúanto había que vender dentro de la empresa ANTIGUAMENTE que el montar modelos de ML...
aportaba mucho valor? HABIA QUE SUDAR PARA VENDER ESTO INTERNAMENTE
Ahora es más fácil...
    1º Porque la industria va en ese camino... SE HA ACEPTADO por la industria.
    2º Más formación / información

Vender Kubernetes hace años... era COMPLICADISIMO:
    1º Porque la industria todavía no estaba alli.. no voy a ser el primer pringao
    2º Mis administradores de sistemas no sabían de eso
    3º Sindicatos! Que ahora vas a despedir a 500 administradores de sistemas? porque ese trabajo lo va a hacer kuebrnetes? 

Hoy en día todo el mundo está con Kubernetes

Con DEVOPS nos pasa igual! Ahora mismo cuesta! (En España y en algunas empresas)
    Fuera de España... y dentro de España en ciertas empresas... están con esto desde hace años!

Y esto ahora... llevado al mundo De los datos! como cierro el círculo
Los datos que uso para el modelo... automatizar su captura
    Capturar datos de producción
    Procesamiento de ese dato para dejarlo listo para el modelo!
    Arranca lo de arriba !
    

Twitter (X)
Facebook
Youtube
TikTok

    Están aplicando esto en tiempo real.
        Van generando modelos sobre la marcha que le muestran a cada usuario lo que va a querer consumir en un momento dado..
        retroalimentandose de lo que están consumiendo (de su historial de consumo... hora del día... día de la semana)...
        
Ni los autores/desarrolladores de los modelos saben cómo funcionan.

Todo esto, para su adopción necesito equipos multidisciplinares!
    DEVOPS -> Linkedin
        Administrador de sistemas v2:
            Linux                       scripts sh -> ansible
            Windows
            Clouds  - Azure             manubrio -> terraform
                    - AWS
                                        -> kubernetes
        Desarrolladores v2
            maven
            poetry
            docker
        Tester v2                       -> Selenium, .... 
    
    Figura nueva: Tipo que configura el Jenkins o similar : DEVOPS
        
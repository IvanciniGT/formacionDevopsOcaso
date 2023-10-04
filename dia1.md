
# Ejecución de un proyecto de desarrollo de un software

Cómo controlo, gestiono ese proyecto?
Antiguamente seguíamos lo que llamábamos una METODOLOGÍA TRADICIONAL: Metodologías waterfall (en cascada) y variantes (V, espiral)

## Metodologías tradicionales

Toma de requisitos -> Análisis -> Diseño -> Desarrollo -> Pruebas -> Implantación -> Mantenimiento
                                                            ^
                                                            Al finalizar el desarrollo (1,5 años después del comienzo del proyecto)
El problema grande aquí era la falta de feedback, de comunicación entre el cliente y el equipo de desarrollo. 
El cliente no veía nada hasta el final del proyecto, y cuando lo veía, no era lo que esperaba.

## Estas metodologías poco a poco han sido reemplazadas por lo que hoy llamamos METODOLOGÍAS ÁGILES

SCRUM, XP, Kanban, Lean, Crystal, FDD, DSDM, ASD, etc...

Que se basan en entregar incrementalmente el producto final.
Dia 15 -> Entrega 1 en producción +30% de la funcionalidad
    Pruebas de paso a producción 30% de la funcionalidad
Dia 30 -> Entrega 2 en producción +20% de la funcionalidad
    Pruebas de paso a producción 20% de la funcionalidad + 30% de la funcionalidad
Dia 45 -> Entrega 2 en producción +20% de la funcionalidad
    Pruebas de paso a producción 20% + 20% + 30% de la funcionalidad

Las metodologías ágiles han traído sus propios problemas nuevos.
- Las pruebas se multiplican!
- Las instalaciones se multiplican (cada 15-30 días tengo una)... que implica a su vez: Instalación en entornos Q&A, PREPRODUCCIÓN, PRODUCCIÓN

De donde saco la pasta? recursos? tiempo? No la hay!
La solución solo pasa por: AUTOMATIZAR

## Cómo gestionábamos el ciclo de vida de un producto de software

Aquí no miro un proyecto... Me centro en el producto de software.
Ese producto está vivo! y tiene un ciclo de vida.
El producto nace... y en algún momento morirá.
Pero no se cuando.
En un momento dado saco una versión del producto... 
y más adelante una nueva versión... y más adelante otra nueva versión...

---

## JIRA y Confluence: Tienen poco que ver con DEVOPS... casi nada.

- JIRA: Herramienta de gestión de proyectos
- CONFLUENCE: Es una herramienta para documentar un proyecto de software

# DEV--->OPS ?

No es una metodología al uso... es más una filosofía de trabajo, cultura, un movimiento... en pro de la AUTOMATIZACION... automatización de qué?
De todas la tareas que tengo entre el desarrollo y la operación de un sistema.

√ Visión acerca de cómo gestionar un activo de software ... desde el desarrollo hasta la operación
√ Procesos de automatización e integración con equipos TI
√ Forma de gestión del ciclo de vida de un software (pruebas, desarrollo, implantación...)

Un proyecto va a estar en las siguiente fases de por vida:                                          AUTOMATIZABLE?              HERRAMIENTAS

- Plan          (Planificación de tareas que necesito realizar)                                         POCO 
                    La puedo hacer con una herramienta que me ayude a llevarla o en papel
                    MSProject, JIRA
- Code          (Análisis, diseño y desarrollo del código)                                              POCO (cada vez más)
                    ---> El código lo dejan en un repositorio de un sistema de control de código fuente
                            CVS
                            Rational IBM
                            SVN
                            GIT*
                                Requiere de un servidor de alojamiento de repos remotos:
                                    - Github
                                    - Gitlab
                                    - Bitbucket
- Build         (Compilar, Empaquetar, etc...)                                                          SI (MUCHO)
                Generar el artefacto del proyecto
                    Instalable
                    Script
                    Imagen de contenedor
                                                                                                                                JAVA: Maven, Gradle, SBT
                                                                                                                                JS:   Npm, Yarm, Webpack
                                                                                                                                .net: MSBuild, nuget, dotnet
                                                                                                                                python: Poetry, pip, setuptools
                                                                                                                                contenedores: Docker, Podman, Buildah
                                                                                                                                script bash, powershell
-----------> Si consigo automatizar hasta este punto -------------------->  Hacer un desarrollo ágil
- Test          (Pruebas)                                                                           
    Diseño de la prueba                                                                                 POCO
    Ejecución de la prueba                                                                              SI (MUCHO)
        Hay pruebas cuya ejecución no es automatizable por naturaleza:  Una prueba de experiencia de usuario UX, Seguridad
        El resto... casi todas... otra cosa es que me cueste mucho o poco hacerlo!
                                                                                                                                Frameworks de pruebas: JUnit, UnitTest, MSTest
                                                                                                                                Web: Selenium, Cypress, Puppeteer, Karka
                                                                                                                                Servicios Web: Postman, SoapUI, RestAssured
                                                                                                                                Rendimiento: JMeter, Gatling, Locust
        ¿Dónde las hacemos?
            - En la máquina del desarrollador? Ni de coña, ya que no me fio de su entorno... está maleao!
            - En la máquina del tester? Tampoco, ya que no me fio de su entorno... está maleao!
            - En un entorno de pre (test) precreado? Tampoco, ya que no me fio de su entorno... está maleao! LA TENDENCIA ES QUE TAMPOCO !
            HOY en día la tendencia es ha crear entornos de pruebas de usar y tirar! como lo klenex!
            Donde me asegure que la instalación no queda maleada y que el entorno no está maleado -> CONTENEDORES
                                                                                                  -> CLOUD
-----------> Si consigo automatizar hasta este punto -------------------->  Pipeline de Integración Continua
Si consigo tener continuamente la última versión del código empaquetado de mis desarrolladores en un entorno de pruebas sometido a pruebas automatizadas

- Release       (El acto de poner en manos de mi cliente una versión-release- de mi producto)           SI                      Hay que subirlo a un Artifactory, Web, FTP,
                                                                                                                                Docker hub, JFrog, NEXUS
                                                                                                        Scripts (sh, bat, ps1, py)
                                                                                                        Librerías específicas
------------> Si consigo automatizar hasta este punto -------------------->  Pipeline de Entrega Continua (Continuous Delivery)
- Deploy        (El acto de instalar una release en un entorno de producción)                           SI
                Otra cosa será la forma de decidir si/o cuando una release debe instalarse en 
                el entorno de producción.
                    La instalación en el entorno de prod requiere lo primero: DE UN ENTORNO DE PRODUCCIÓN
                    Y ese entorno hoy en día la tendencia es a crearlo bajo demanda.
                        Y es más... si paso de una versión a otra de mi producto, tiro el entono de prod anterior a la basura y creo uno nuevo. -> CONTENEDORES
                                                                                                                                                -> CLOUD
                Tanto como que todas las empresas está llevando sus entornos de producción Kubernetes (Distribución de Kubernetes: K8S, K3S, Openshift(Redhat), Tanzu(VMWare), Rancher(Suse), EKS(Amazon), GKE(Google), AKS(Microsoft))

                Hoy en día quien se encarga de instalar apps en el entorno de prod es Kubernetes... a eso vamos.
                Si no.. y sigo con despliegues más tradicionales, también automatizo: .sh, yum, apt, msi
                Terraform: Me permite adquirir infra nueva programaticamente (CLOUDs)
                Ansible: Me permite configurar la infra programaticamente (CLOUDs)
------------> Si consigo automatizar hasta este punto -------------------->  Pipeline de Despliegue Continuo (Continuous Deployment)
- Operation     (La operación de mi producto en el entorno de producción)                               SI
                    Controlar caídas de servicio (reiniciar, etc...)
                    Escalado de una aplicativo
                    Lanzamiento con unas periodicidades de tareas
                    Backups -> Restore
                Hoy en día está en manos de Kubernetes (Google... para todo su entorno de producción)
- Monitor       (Extraer información en tiempo real)                                                    SI
                    - Tiempos de disponibilidad
                    - Logs, donde identificar errores o problemas
                    - Extraer otras informaciones valiosas desde el punto de vista de negocio
                                                                                                                                Kubernetes / Docker
                                                                                                                                Prometheus / Grafana
                                                                                                                                ElasticSearch / Kibana


Estamos hablando aquí arriba de lo que llamamos automatizaciones de nivel 1.
Si hubiera automatizado todas las tareas de este tipo que necesita(uso) en mi proyecto, hay algo más que necesitaría automatizar?
La ejecución(y orquestación) de esas automatizaciones: Automatización de segundo nivel: JENKINS, GITLAB CI/CD, AZURE DEVOPS, GITHUB ACTIONS, CIRCLECI, TRAVIS, TEAMCITY, BAMBOO, etc...
---

# Automatizar en nuestro contexto:

Montar un programa(hardware) que haga lo que nosotros hacíamos antes a mano.

---
Producto de software A, del que genero 1 versión y me olvido de ella! 
Tiene sentido aquí automatizar? Puede ser... por ejemplo estoy trabajando cada mes en un proyecto... totalmente independiente de otro, pero que lo gestiono de la misma forma.

Puedo usar (abrazar) una cultura devops sin necesidad de ir a una metodología ágil.
Lo contrario es muy complejo.
---

# Tipos de software

Hay muchos tipos de software:
- Sistema Operativo
- Driver
- Librería
- Aplicación
- Demonios
- Servicios
- Scripts
- Comandos

---

# GIT

Es un sistema de control de código fuente distribuido.
Un proyecto en git, es la unión de todos sus repositorios... que habrá muchos.
Ningún repositorio por si solo contiene toda la información del proyecto.

Eso es diferente por ejemplo en : ClearCase, CVS, SVN, Rational IBM, etc... Éstos son sistemas de control de código fuente centralizados.

## Repositorio

Es el conjunto commits distribuidos en ramas, asociados a un proyecto de software.

## Commit en git

En CVS o Subversion un Commit era un conjunto de cambios que aplicaba a mi código.
En git no. ni parecido. Es más simple:
Es un backup INTEGRAL (completo) de mi proyecto en un momento dado del tiempo.
Lo mismo que si cojo la carpeta de mi proyecto, botón derecho del ratón: METER EN ARCHIVO ZIP.

Lo que vamos guardando en un repositorio es una SECUENCIA de commits... de copias de seguridad.
Qué aporta un Sistema de control de versiones como GIT frente a un sistema de copias de seguridad? LAS RAMAS (Branches)

## Ramas en SCM

Una linea de evolución en el tiempo de mi código... paralela a otras lineas de evolución.

En ocasiones, querremos ver los cambios que se introdujeron en una versión. Ese en git se calcula BAJO DEMANDA, comparando una copia con la anterior... o con otra que haya por ahí.

Cuando trabajamos con GIT, cada persona del proyecto tiene SU PROPIO REPOSITORIO, diferente al del resto de personas.

        Clientes
              |                       RAMA_Master
        Rama_MASTER                   RAMA_Des   C1 > C2 > C3
        REMOTO2 GITHUB                REPO REMOTO 1 BITBUCKET
              |                       Servidor (HTTP, ssh): BitBucket[servicio + on premisses] | gitlab[servicio + on premisses] | github[servicio]
              |                              |
---------------------------------------------------------------------------------------------------------------------------------- RED DE MI EMPRESA
 |                                                                                                                      |
 IvanPC                                                                                                             MenchuPC
 |- Proyecto1/  (Working directory)                                                                                     |- Proyecto1/  (Working directory)
 |    |.git/ Contiene mi repo y mi carpeta Staging                                                                      |    |-src/
 |    |- src/                                                                                                           |       |- modelo.py (v3m) -> Staging
 |        |- modelo.py (v3i=v4)              -> Lo copio a la carpeta de staging (GIT ADD)                              |- .git/ Contiene mi repo y mi carpeta Staging
 |                                                                                                                          RAMA_MENCHU C1 > C2 -> C3
 |                                                                                                                             ^            (GIT MERGE, GIT REBASE)
 |- Staging del Proyecto1/  -> De la que en un momento dado                                                                 RAMA_Des   C1 > C2 > C3
 |     |- src/                 hago una copia de seguridad (GIT COMMIT)                                                                 ^   (GIT FETCH)
 |        |- modelo.py (v3i=v4)                                                                                                Copia RAMA_Des(del remoto): C1  > C2
 |                             Esa copia la guardaré en una RAMA (branch) de mi repositorio local.                               (se actualiza desde el remoto)
 |.git (repo local)
    RAMA_Ivan C1 (...modelo.py(v1)) > C2 (...modelo.py(v2)) > C3 (...modelo.py(v3)) > C4(...modelo.py(v3i+v3m=v4)
                                      v                                             / git merge | git rebase
    RAMA_Des  C1                    > C2 > C3(menchu: modelo.py(v3m))---------------
                                      v
    COPIA RAMA_Des(del remoto): C1  > C2 > C3 La sincronizo con el remoto (GIT PUSH)

La sincronización entre un repo remoto en git y un local siempre se hace mediante RAMAS.

    GIT PULL: Es un GIT FETCH + (GIT MERGE | GIT REBASE)


Git add         Copiar cosas al área de staging
Git commit      Copiar cosas del área de staging al repositorio localGenerar una copia de seguridad de mi carpeta (staging) dentro de la rama en la que me encuentre
Git push        Sincronizar mi rama (en la que estoy) con una rama del repositorio remoto
Git fetch       Sincronizar una rama del repositorio remoto con una rama de mi repositorio local
Git merge | git rebase      Sincronizar una rama de mi repositorio local con otra rama de mi repositorio local
Git pull        git fetch + (git merge | git rebase)

# Cuando trabajamos con GIT, lo primero y MAS IMPORTANTE DE TODO EN EL MUNDO MUNDIAL, es definir el GITFLOW que voy a utilizar.

Esto es la madre del cordero... no solo para GIT, sino para poder hacer en el futuro AUTOMATIZACIONES (DEVOPS: CI+CD...)

MASTER / MAIN (Trunk) -> Rama principal de mi proyecto
    REGLA DE ORO DE ESTA RAMA: Nunca jamás bajo pena capital puedo hacer un commit en esta rama... solo puedo copiar commits de otras ramas a esta.
    Todo lo que hay en esta rama se considera LISTO PARA PRODUCCIÓN!
   ^ En este cambio de estado, se deben superar todas lass pruebas de sistema
RELEASE
   ^ En este cambio de estado (Aquí se deben pasar todas las pruebas de integración)
DEVELOP -> Esta es en la que integramos los cambios que hace el equipo (en vuestro caso, el equipo suele ser 1 persona)
Si tengo varias personas en un proyecto, lo habitual es:
    - O crear ramas por persona
    - O crear ramas por features (características del software que estoy montando)
    RAMA FEATURE 1 -> Alimentaríamos la rama DEVELOP
    RAMA FEATURE 2 -> Alimentaríamos la rama DEVELOP (en estos cambios de ramas, sería necesario superar las pruebas UNITARIAS)

Este flujo de trabajo es el que me permitiría ahora automatizar trabajos.
 Cada vez que se copie un commit de una RAMA FEATURE a la RAMA DEVELOP: Necesito que validen las pruebas UNITARIAS ( Y ES ALGO QUE CONFIGURARÉ EN JENKINS)
 Cada vez que lo que tengo en DEVELOP lo mando a RELEASE: Necesito que validen las pruebas de INTEGRACIÓN ( Y ES ALGO QUE CONFIGURARÉ EN JENKINS)
 Cada vez que lo que tengo en RELEASE lo mando a MASTER: Necesito que validen las pruebas de SISTEMA ( Y ES ALGO QUE CONFIGURARÉ EN JENKINS)

Y a partir de ese esquema, vamos simplificando para nuestro escenario de uso.

---

# Pruebas de software

Cualquier prueba sea del tipo que sea, se debe centrar en una única característica del software que están probando.

## Clasificación de las pruebas de software

Se clasifican en base a distintas taxonomías... independendientes entre sí.

### En función al nivel de la prueba

Unitarias:          Pruebas de una característica de un componente AISLADO del sistema. 

                    TREN            Prueba unitaria
                        Motor       Si le meto corriente, se mueve? gira?
                        Ruedas      Si la empujo, se mueve? gira?
                        Freno       Si le meto corriente, cierra las pinzas?
                        Sistema de transmisión (engranajes, cigüeñal, etc...)

Integración:        Prueba la COMUNICACIÓN entre componentes del sistema

                    Junto las ruedas y el freno.
                    Si le meto corriente al freno, y las ruedas están girando, se paran?
                        NO... resuelta que las ruedas son demasiado estrechas y las pinzas no las aprisionan.

End2End(sistema):  Se centran en el COMPORTAMIENTO del sistema como un todo.

                    Tengo el tren montado. Cada componente per se, funciona correctamente.
                    Los componentes entre si, se comunican correctamente.
                    Bien... ahora enciendo el tren, le doy a la palanca... y resuelta que el tren va hacia atrás!!!!

### En función de la naturaleza de la prueba

Funcionales:        Las que se centran en la funcionalidad
No funcionales:     Las que se centran en otros aspectos: Seguridad, Rendimiento, Usabilidad, etc...

### En función de la forma en que se ejecutan:

Dinámicas:          Las que necesitan poner aquello en marcha
Estáticas:          Las que no... por ejemplo: Análisis de calidad de código ----> AUTOMATIZADAS: SonarQube

### Pruebas de regresión

Cualquier prueba antigua que la vuelvo a ejecutar, para ver que no me haya cargado nada de lo que ya funcionaba.
---

# Comandos de Git y más

Un repo de git se puede crear de 2 formas diferentes:
 1. Crear un repo local, en el que cargo archivos

        $ git init

    Crear un repo remoto (sin inicializar) en bitbucket
    Subir lo que tengo en local al remoto
 2. Crear un repo remoto (inicializado) en bitbucket    <<<<<<< Esta es la más utilizada
    Clonar el repo remoto en local
     $ git clone https://ivanciniGT@bitbucket.org/ivanciniGT/pruebaocaso3.git
        Internamente, me hace:
             git init para crear un repo local
             git remote add origin https://bitbucket.org/ivanciniGT/pruebaocaso3.git
             git push -u origin master (ha creado una rama en mi local copia de la del remoto)
    Crear archivos en local
    Y subir lo que tengo en local al remoto

### Los 3 árboles de git

    $ git status
        Me permite saber las diferencias (a alto nivel, a nivel de archivos) entre lo que hay :
                          <-ENTRE ESTOS->                   <- ENTRE ESTOS ->            <- ENTRE ESTOS ->
                       Cambios no rastreados           cambios para ser confirmados
    <---------------------------- Mi máquina ------------------------------------->                     <-- BitBucket -->
    WORKING DIR (mi carpeta)   <>   AREA DE PREPARACION (Staging)   <>   REPO LOCAL             <>         REPO REMOTO
      dia1.md(v3)                         dia1.md(v3)                      ZIP(dia1.md(v1))
                                                                           ZIP(dia1.md(v3)) < HEAD
                    git add dia1.md                        git commit -m "MENSAJE"
                    git add * (sin incluir ocultos)
                    git add . (incluyendo ocultos)
                                                           < git diff --cached >
                       < git diff >
                       <                 git diff head                         >
                                                                                            git push ->
                                                                                            <- git fetch
                                                                                   Sincroniza mi copia de la rama remota         
                                                                                  
                                                                        git merge remotes/origin/master
                                                                        Sincroniza mi copia de la rama remota con mi rama
                                                                                            <- git pull (git fetch + git merge)
                                                                        Sincroniza mi rama con la remota
                                                                                    

### LA VARIABLE HEAD

Indica que commit es el que estoy visualizando en mi directorio de trabajo. HABITUAMENTE coincide (y por defecto es así) con el último commit que tengo en el REPO LOCAL

Para mover la cabeza (HEAD) de un commit a otro, usamos

    $ git checkout ID_DEL_COMMIT

### HISTORIAL

Consultar el historial del proyecto

    $ git log --oneline --all --graph

#### Consultar diferencias a bajo nivel entre versiones de un archivo:

    $ git diff 257981f 959d0ee dia1.md
    $ git diff HEAD HEAD~2

### Remotos en git

    $ git remote            Listado de remotos con los que trabajo
    $ git remote add <nombre> <url>  Añadir un nuevo remoto
                     origin          Al primer remoto (al principal)
    $ git remote remove <nombre>     Eliminar un remoto

### Trabajando con remotos:

$ git push -u origin master
    Solo se ejecuta la primera vez que mando una rama a un remoto
    - Crea la rama en el remoto
    - Crea una copia de la rama del remoto en mi máquina local
    - Copia lo que tengo en mi rama (master) a la copia que tengo en local de la del remoto
    - Manda mi copia de la del remoto al remoto

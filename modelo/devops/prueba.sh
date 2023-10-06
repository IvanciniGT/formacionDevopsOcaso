docker build . -f Dockerfile -t modelo:test --no-cache

contenedor=$(docker run \
    --rm \
    -v $PWD/../data/paragraphs:/datos \
    -v $PWD/../src:/codigo \
    -v $PWD/../target:/exportacion \
    -d \
    modelo:test \
    sleep 3600)

# Aquí podría ejecutar pruebas adicionales, antes de meterme en la generación del modelo
docker exec $contenedor ls /datos/ar

# Y ya me meto en la generaicón del modelo
docker exec $contenedor python generar_modelo.py --export

docker stop $contenedor


ls $PWD/../target/modelo.sav
# Si el fichero no existe, al ejecutar este script, el script acaba con estado ERROR
# Mientras que si el fichero existe, el script acaba con estado OK




#docker run \                                Crea un contenedor... y ejecutalo (docker container create + docker container start)
#    --rm \                                  Y... si el contenedor en algún momento se para... bórralo                  
#    -v $PWD/../data/paragraphs:/datos \     En el contenedor, al acceder a /dato, realmente se accede a mi capreta /data/paragraphs
#    -v $PWD/../src:/codigo \                    "
#    -v $PWD/../target:/exportacion \            "
#    -d \                                    Quiero que la ejecución del contenedor se haga en segundo plano. De no hacer ésto,
#                                            Docker deja bloqueado el entorno (terminal) donde estoy ejecutando este comando... a espera de que concluya
#    modelo:test \                           Imagen que quiero usar para crear el contenedor... LA MIA, que he generado arriba
#    sleep 3600                              Deja el contenedor arrancado sin hacer nada
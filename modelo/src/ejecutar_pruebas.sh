export RUTA_DATOS="../data/paragraphs"
export RUTA_DESTINO_MODELO="../target/modelo.sav"
python modelo_test.py $1 $2
python exportar_modelo_test.py $1 $2
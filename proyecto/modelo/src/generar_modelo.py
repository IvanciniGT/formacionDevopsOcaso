import sys
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Perceptron
from sklearn.pipeline import Pipeline
from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pickle

def prepararDatos(ruta_datos):
    # carga de datos
    dataset = load_files(ruta_datos)
    
    # Preparación de datos
    docs_train, docs_test, y_train, y_test = train_test_split(
        dataset.data, dataset.target, test_size=0.5)

    # Devlver los datos
    return (docs_train, docs_test, y_train, y_test, dataset.target_names)

def validarModelo(modelo, docs_test, y_test, target_names):
        
    y_predicted = modelo.predict(docs_test)
    
    print(metrics.classification_report(y_test, y_predicted,
                                        target_names=target_names))
    
    cm = metrics.confusion_matrix(y_test, y_predicted)
    print(cm)


def generarModelo(docs_train, y_train):
    
    
    # Generación del modelo
    vectorizer = TfidfVectorizer(ngram_range=(1, 4),
                                 use_idf=True)
    clf = Pipeline([
        ('vec', vectorizer),
        ('clf', Perceptron(tol=1e-9)),
    ])
    
    # Ajuste / Entrenamiento
    clf.fit(docs_train, y_train)
    
    return clf

def exportarModelo(modelo, ruta_destino_modelo):
    # Exportar el modelo
    if not os.path.exists(ruta_destino_modelo):
        os.makedirs(ruta_destino_modelo)
    fichero = open(ruta_destino_modelo+"/modelo.sav", 'wb')
    pickle.dump(modelo, fichero)
    fichero.close()

if __name__ == '__main__':
    RUTA_DATOS = os.getenv('RUTA_DATOS')
    RUTA_DESTINO_MODELO = os.getenv('RUTA_DESTINO_MODELO') 
    # Cargando datos
    (docs_train, docs_test, y_train, y_test, target_names) = prepararDatos(RUTA_DATOS)
    # Generando modelo
    modelo = generarModelo(docs_train, y_train)
    if "--validate" in sys.argv:
        validarModelo(modelo, docs_test, y_test, target_names)
    if "--export" in sys.argv:
        exportarModelo(modelo,RUTA_DESTINO_MODELO )

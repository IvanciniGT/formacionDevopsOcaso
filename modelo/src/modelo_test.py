import unittest
import os
from generar_modelo import prepararDatos, generarModelo
class CreacionModeloTest(unittest.TestCase):
    
    def test_creacion_modelo(self):
        RUTA_DATOS = os.getenv('RUTA_DATOS')
        RUTA_DESTINO_MODELO = os.getenv('RUTA_DESTINO_MODELO') 
        # Cargando datos
        (docs_train, docs_test, y_train, y_test, target_names) = prepararDatos(RUTA_DATOS)
        # Generando modelo
        #print() # Esto sería el log
        # Habitualmente trabajo con un logger ... que en caso de que mi programa se ejecute e un contenedor le pongo como fichero de salida: /proc/1
        modelo = generarModelo(docs_train, y_train)
        # Hago una prueba
        self.assertEqual('en', target_names[modelo.predict(['This is a language detection test for the training.'])[0]])
        self.assertEqual('de', target_names[modelo.predict(['Dies ist ein Test, um die Sprache zu erkennen.'])[0]])
        self.assertEqual('es', target_names[modelo.predict(['Esto es un test de detección de idiomas para el curso.'])[0]])

if __name__ == '__main__':
    unittest.main()

import unittest
import os
import pickle

from generar_modelo import prepararDatos, generarModelo, exportarModelo
class CreacionModeloTest(unittest.TestCase):
    
    def test_exportacion_modelo(self):
        RUTA_DATOS = os.getenv('RUTA_DATOS')
        RUTA_DESTINO_MODELO = os.getenv('RUTA_DESTINO_MODELO') 
        # Cargando datos
        (docs_train, docs_test, y_train, y_test, target_names) = prepararDatos(RUTA_DATOS)
        # Generando modelo
        modelo = generarModelo(docs_train, y_train)
        # Exporto el modelo
        exportarModelo(modelo, RUTA_DESTINO_MODELO )
        
        # Importarlo
        fichero = open(RUTA_DESTINO_MODELO, 'rb')
        modelo_exportado = pickle.load(fichero+"/modelo.sav")
        fichero.close()

        # Hago una prueba
        self.assertEqual('en', target_names[modelo_exportado.predict(['This is a language detection test for the training.'])[0]])
        self.assertEqual('de', target_names[modelo_exportado.predict(['Dies ist ein Test, um die Sprache zu erkennen.'])[0]])
        self.assertEqual('es', target_names[modelo_exportado.predict(['Esto es un test de detección de idiomas para el curso.'])[0]])

if __name__ == '__main__':
    unittest.main()

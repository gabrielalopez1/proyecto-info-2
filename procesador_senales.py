import scipy.io
import numpy as np

class ProcesadorSenales:
    def __init__(self):
        pass

    def cargar_mat(self, ruta):
        """Carga un archivo .mat y devuelve el diccionario de datos"""
        try:
            data = scipy.io.loadmat(ruta)
            return data
        except Exception as e:
            print(f"Error al cargar archivo .mat: {e}")
            return None

    def obtener_llaves_validas(self, data):
        """Obtiene las llaves que no son metadatos del archivo .mat"""
        llaves = [key for key in data.keys() if not key.startswith('__')]
        return llaves

    def extraer_array(self, data, llave):
        """Devuelve el array asociado a la llave, o None si la llave no es válida"""
        try:
            array = data[llave]
            if isinstance(array, np.ndarray):
                return array
            else:
                return None
        except Exception as e:
            print(f"Error al extraer arreglo: {e}")
            return None

    def calcular_promedio(self, array, eje=1):
        """Calcula el promedio a lo largo del eje especificado"""
        try:
            promedio = np.mean(array, axis=eje)
            return promedio
        except Exception as e:
            print(f"Error al calcular promedio: {e}")
            return None



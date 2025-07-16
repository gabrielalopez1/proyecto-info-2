import pandas as pd

class ProcesadorCSV:
    def __init__(self):
        pass

    def cargar_csv(self, ruta):
        try:
            df = pd.read_csv(ruta)
            return df
        except Exception as e:
            print(f"Error al cargar CSV: {e}")
            return None


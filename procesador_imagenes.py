import pydicom
import nibabel as nib
import cv2
import numpy as np
import os



class ProcesadorImagenes:
    def __init__(self):
        pass

    def cargar_carpeta_dicom(self, carpeta):
        slices = []
        for archivo in os.listdir(carpeta):
            ruta_archivo = os.path.join(carpeta, archivo)
            try:
                ds = pydicom.dcmread(ruta_archivo)
                if hasattr(ds, 'InstanceNumber'):
                    slices.append(ds)
            except Exception as e:
                continue  # Ignora archivos no DICOM

        # Ordenar por número de imagen (InstanceNumber)
        slices.sort(key=lambda x: int(x.InstanceNumber))

        # Crear volumen 3D
        volumen = np.stack([s.pixel_array for s in slices], axis=0)
        return volumen, slices[0]  # Devolver volumen y un header de referencia
     

    def convertir_dicom_a_nifti(self, carpeta_dicom, ruta_salida_nifti):
        slices = []
        for archivo in sorted(os.listdir(carpeta_dicom)):
            ruta_archivo = os.path.join(carpeta_dicom, archivo)
            try:
                ds = pydicom.dcmread(ruta_archivo)
                slices.append(ds.pixel_array)
            except:
                continue

        if slices:
            volumen = np.stack(slices, axis=0)
            nifti_img = nib.Nifti1Image(volumen, affine=np.eye(4))
            nib.save(nifti_img, ruta_salida_nifti)
            print(f"✅ Carpeta DICOM convertida a NIfTI: {ruta_salida_nifti}")




    def cargar_imagen_normal(self, ruta):
        imagen = cv2.imread(ruta)
        return imagen
    
    def convertir_grises(self, imagen):
        return cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        
    def ecualizar_histograma(self, imagen_gris):
        return cv2.equalizeHist(imagen_gris)
    
    def binarizar(self, imagen_gris, threshold=127):
        _, binaria = cv2.threshold(imagen_gris, threshold, 255, cv2.THRESH_BINARY)
        return binaria

    def morfologia(self, imagen_binaria, operacion='cierre',kernel_size=5):
        if kernel_size % 2 == 0:
            kernel_size += 1
        kernel = np.ones((kernel_size, kernel_size), np.uint8)



        if operacion == 'cierre':
            return cv2.morphologyEx(imagen_binaria, cv2.MORPH_CLOSE, kernel)
        elif operacion == 'apertura':
            return cv2.morphologyEx(imagen_binaria, cv2.MORPH_OPEN, kernel)
        else:
            return imagen_binaria

    def contar_celulas(self, imagen_binaria):
        contornos, _ = cv2.findContours(imagen_binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return len(contornos), contornos
    
    def aplicar_clahe(self, imagen_gris):
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        return clahe.apply(imagen_gris)












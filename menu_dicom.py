from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog, QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from modelo.procesador_imagenes import ProcesadorImagenes
from modelo.modelo_datos import ModeloDatos
import numpy as np
import cv2

class MenuDicom(QWidget):
    def __init__(self,modelo):
        super().__init__()
        self.modelo = modelo 
        self.setWindowTitle("Visualización 3D DICOM")
        self.procesador = ProcesadorImagenes()
        self.volumen = None
        self.init_ui()
        self.setStyleSheet("""
    QWidget {
        background-color: #f0f4f7;
        font-family: 'Segoe UI', sans-serif;
        font-size: 12pt;
    }

    QLabel {
        color: #2c3e50;
        font-weight: bold;
    }

    QLineEdit, QComboBox, QTableView {
        background-color: #ffffff;
        border: 1px solid #ccc;
        border-radius: 6px;
        padding: 6px;
    }

    QPushButton {
        background-color: #3498db;
        color: white;
        border-radius: 8px;
        padding: 8px 12px;
        font-weight: bold;
    }

    QPushButton:hover {
        background-color: #2980b9;
    }

    QSlider::groove:horizontal {
        background: #dcdde1;
        height: 6px;
        border-radius: 4px;
    }

    QSlider::handle:horizontal {
        background: #3498db;
        width: 16px;
        margin: -5px 0;
        border-radius: 8px;
    }

    QHeaderView::section {
        background-color: #3498db;
        color: white;
        padding: 4px;
        border: none;
    }
""")


    def init_ui(self):
        self.label_info = QLabel("Cargar carpeta DICOM para ver cortes")
        self.btn_cargar = QPushButton("Cargar Carpeta DICOM")
        self.btn_cargar.clicked.connect(self.cargar_carpeta)
        
        self.btn_convertir_nifti = QPushButton("Convertir a NIfTI")
        self.btn_convertir_nifti.clicked.connect(self.convertir_a_nifti)

        self.label_imagen = QLabel()
        self.label_imagen.setFixedSize(400, 400)

        self.slider_axial = QSlider(Qt.Horizontal)
        self.slider_coronal = QSlider(Qt.Horizontal)
        self.slider_sagital = QSlider(Qt.Horizontal)

        self.slider_axial.valueChanged.connect(self.actualizar_corte)
        self.slider_coronal.valueChanged.connect(self.actualizar_corte)
        self.slider_sagital.valueChanged.connect(self.actualizar_corte)

        layout = QVBoxLayout()
        layout.addWidget(self.label_info)
        layout.addWidget(self.btn_cargar)
        layout.addWidget(self.btn_convertir_nifti)
        layout.addWidget(self.label_imagen)
        layout.addWidget(QLabel("Corte Axial"))
        layout.addWidget(self.slider_axial)
        layout.addWidget(QLabel("Corte Coronal"))
        layout.addWidget(self.slider_coronal)
        layout.addWidget(QLabel("Corte Sagital"))
        layout.addWidget(self.slider_sagital)

        self.setLayout(layout)

    def cargar_carpeta(self):
        carpeta = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta DICOM")
        if carpeta:
            volumen, ds = self.procesador.cargar_carpeta_dicom(carpeta)
            if volumen is not None:
                self.volumen = volumen
                self.slider_axial.setMaximum(volumen.shape[0] - 1)
                self.slider_coronal.setMaximum(volumen.shape[1] - 1)
                self.slider_sagital.setMaximum(volumen.shape[2] - 1)
                self.actualizar_corte()

                # ✅ Registrar en base de datos
                nombre = carpeta.split("/")[-1]
                self.modelo.registrar_archivo("DICOM", nombre, carpeta)

    def actualizar_corte(self):
        if self.volumen is None:
            return

        axial_idx = self.slider_axial.value()
        coronal_idx = self.slider_coronal.value()
        sagital_idx = self.slider_sagital.value()

        corte = self.volumen[axial_idx, :, :]
        if self.sender() == self.slider_coronal:
            corte = self.volumen[:, coronal_idx, :]
        elif self.sender() == self.slider_sagital:
            corte = self.volumen[:, :, sagital_idx]

        img_norm = cv2.normalize(corte, None, 0, 255, cv2.NORM_MINMAX)
        img_uint8 = img_norm.astype(np.uint8)
        h, w = img_uint8.shape
        qimg = QImage(img_uint8.data, w, h, w, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(qimg).scaled(400, 400, Qt.KeepAspectRatio)
        self.label_imagen.setPixmap(pixmap)


    def convertir_a_nifti(self):
        carpeta = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta DICOM")
        if carpeta:
            ruta_salida, _ = QFileDialog.getSaveFileName(self, "Guardar NIfTI", "", "NIfTI files (*.nii)")
            if ruta_salida:
                self.procesador.convertir_dicom_a_nifti(carpeta, ruta_salida)
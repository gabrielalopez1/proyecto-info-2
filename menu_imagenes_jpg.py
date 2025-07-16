from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QComboBox, QSlider
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from modelo.modelo_datos import ModeloDatos
import cv2
from modelo.procesador_imagenes import ProcesadorImagenes
import numpy as np

class MenuImagenesJPG(QWidget):
    def __init__(self,modelo):
        super().__init__()
        self.modelo = modelo
        self.setWindowTitle("Procesamiento de Imágenes JPG/PNG")
        self.procesador = ProcesadorImagenes()
        self.imagen = None
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
        self.label_imagen = QLabel("Imagen Original")
        self.label_imagen.setFixedSize(300, 300)

        self.btn_cargar = QPushButton("Cargar Imagen")
        self.btn_cargar.clicked.connect(self.cargar_imagen)

        self.btn_grises = QPushButton("Grises")
        self.btn_grises.clicked.connect(self.mostrar_grises)

        self.btn_ecualizar = QPushButton("Ecualizar")
        self.btn_ecualizar.clicked.connect(self.mostrar_ecualizada)

        self.btn_binarizar = QPushButton("Binarizar")
        self.btn_binarizar.clicked.connect(self.mostrar_binaria)
        
        self.btn_morfologia = QPushButton("Morfología (Cierre)")
        self.btn_morfologia.clicked.connect(self.mostrar_morfologia)
        
        self.btn_apertura = QPushButton("Morfología (Apertura)")
        self.btn_apertura.clicked.connect(self.mostrar_apertura)

        self.slider_kernel = QSlider(Qt.Horizontal)
        self.slider_kernel.setMinimum(1)
        self.slider_kernel.setMaximum(15)
        self.slider_kernel.setValue(5)
        self.slider_kernel.setTickInterval(2)
        self.slider_kernel.setTickPosition(QSlider.TicksBelow)
        
        self.btn_contar = QPushButton("Contar Células")
        self.btn_contar.clicked.connect(self.contar_celulas)

        self.btn_clahe = QPushButton("Aplicar CLAHE (Método Nuevo)")
        self.btn_clahe.clicked.connect(self.aplicar_clahe)

        layout = QVBoxLayout()
        layout.addWidget(self.label_imagen)
        layout.addWidget(self.btn_cargar)
        layout.addWidget(self.btn_grises)
        layout.addWidget(self.btn_ecualizar)
        layout.addWidget(self.btn_binarizar)
        layout.addWidget(QLabel("Tamaño de Kernel:"))
        layout.addWidget(self.slider_kernel)
        layout.addWidget(self.btn_morfologia)
        layout.addWidget(self.btn_apertura)
        layout.addWidget(self.btn_contar)
        layout.addWidget(self.btn_clahe)

        self.setLayout(layout)

    def cargar_imagen(self):
        try:
            ruta, _ = QFileDialog.getOpenFileName(self, "Abrir Imagen", "", "Imágenes (*.png *.jpg *.jpeg)")
            if ruta:
                print("Ruta seleccionada:", ruta)  # Verifica que sí seleccionas algo

                self.imagen = self.procesador.cargar_imagen_normal(ruta)
                print("Imagen cargada:", self.imagen is not None)

                if self.imagen is None:
                    print("❌ No se pudo cargar la imagen.")
                    return

                self.mostrar_imagen(self.imagen)

                nombre = ruta.split("/")[-1]
                self.modelo.registrar_archivo("JPG/PNG", nombre, ruta)
                print("✅ Imagen registrada en base de datos.")

        except Exception as e:
            print("❌ Error general en cargar_imagen:", e)
    


    def mostrar_grises(self):
        if self.imagen is not None:
            gris = self.procesador.convertir_grises(self.imagen)
            self.mostrar_imagen(gris)

    def mostrar_ecualizada(self):
        if self.imagen is not None:
            gris = self.procesador.convertir_grises(self.imagen)
            eq = self.procesador.ecualizar_histograma(gris)
            self.mostrar_imagen(eq)

    def mostrar_binaria(self):
        if self.imagen is not None:
            gris = self.procesador.convertir_grises(self.imagen)
            binaria = self.procesador.binarizar(gris)
            self.mostrar_imagen(binaria)

    def mostrar_morfologia(self):
        if self.imagen is not None:
            gris = self.procesador.convertir_grises(self.imagen)
            binaria = self.procesador.binarizar(gris)
            k = self.obtener_kernel()
            morfo = self.procesador.morfologia(binaria, operacion='cierre',kernel_size=k)
            self.mostrar_imagen(morfo)
            print("✅ Morfología aplicada")

    def mostrar_apertura(self):
        if self.imagen is not None:
            gris = self.procesador.convertir_grises(self.imagen)
            binaria = self.procesador.binarizar(gris)
            k = self.obtener_kernel()
            morfo = self.procesador.morfologia(binaria, operacion='apertura', kernel_size=k)
            self.mostrar_imagen(morfo)
            print(f"✅ Morfología Apertura aplicada (Kernel: {k}x{k})")        

    def contar_celulas(self):
        if self.imagen is not None:
            gris = self.procesador.convertir_grises(self.imagen)
            binaria = self.procesador.binarizar(gris)
            k = self.obtener_kernel()
            morfo = self.procesador.morfologia(binaria,  kernel_size=k)
            n, contornos = self.procesador.contar_celulas(morfo)

            imagen_contornos = cv2.cvtColor(gris, cv2.COLOR_GRAY2BGR)
            cv2.drawContours(imagen_contornos, contornos, -1, (0, 255, 0), 2)

            self.mostrar_imagen(imagen_contornos)
            self.setWindowTitle(f"Células detectadas: {n}")
            print(f"✅ Células detectadas: {n}(Kernel: {k}x{k})")

    def aplicar_clahe(self):
        if self.imagen is not None:
            gris = self.procesador.convertir_grises(self.imagen)
            clahe_img = self.procesador.aplicar_clahe(gris)
            self.mostrar_imagen(clahe_img)


    def mostrar_imagen(self, imagen_cv):
        try:
            if imagen_cv is None:
                print("❌ La imagen está vacía")
                return

            h, w = imagen_cv.shape[:2]

            if len(imagen_cv.shape) == 2:
                qimg = QImage(imagen_cv.data, w, h, w, QImage.Format_Grayscale8)
            else:
                imagen_rgb = cv2.cvtColor(imagen_cv, cv2.COLOR_BGR2RGB)
                qimg = QImage(imagen_rgb.data, w, h, w * 3, QImage.Format_RGB888)

            pixmap = QPixmap.fromImage(qimg).scaled(300, 300, Qt.KeepAspectRatio)
            self.label_imagen.setPixmap(pixmap)

        except Exception as e:
            print("❌ Error en mostrar_imagen:", e)

    def obtener_kernel(self):
        k = self.slider_kernel.value()
        if k % 2 == 0:
            k += 1
        return k
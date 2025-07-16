from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout
from vista.menu_dicom import MenuDicom
from vista.menu_imagenes_jpg import MenuImagenesJPG
from vista.menu_csv import MenuCSV

class MenuImagenes(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú Principal - Experto en Imágenes")
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
        self.btn_dicom = QPushButton("Visualizar Imágenes DICOM")
        self.btn_dicom.clicked.connect(self.abrir_dicom)

        self.btn_jpg = QPushButton("Procesar Imágenes JPG/PNG")
        self.btn_jpg.clicked.connect(self.abrir_jpg)

        self.btn_csv = QPushButton("Visualizar Datos CSV")
        self.btn_csv.clicked.connect(self.abrir_csv)

        layout = QVBoxLayout()
        layout.addWidget(self.btn_dicom)
        layout.addWidget(self.btn_jpg)
        layout.addWidget(self.btn_csv)
        self.setLayout(layout)

    def abrir_dicom(self):
        self.ventana_dicom = MenuDicom()
        self.ventana_dicom.show()

    def abrir_jpg(self):
        self.ventana_jpg = MenuImagenesJPG()
        self.ventana_jpg.show()

    def abrir_csv(self):
        self.ventana_csv = MenuCSV()
        self.ventana_csv.show()

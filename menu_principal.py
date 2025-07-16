from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel
from vista.menu_dicom import MenuDicom
from vista.menu_imagenes_jpg import MenuImagenesJPG
from vista.menu_senales import MenuSenales

class MenuPrincipal(QWidget):
    def __init__(self, modelo):
        super().__init__()
        self.setWindowTitle("Menú Principal BioApp")
        self.modelo = modelo
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
        label = QLabel("Seleccione una opción:")

        self.btn_dicom = QPushButton("Visualizar imágenes DICOM")
        self.btn_jpg = QPushButton("Procesar imágenes JPG/PNG")
        self.btn_csv = QPushButton("Visualizar datos CSV")

        self.btn_dicom.clicked.connect(self.abrir_menu_dicom)
        self.btn_jpg.clicked.connect(self.abrir_menu_jpg)
        self.btn_csv.clicked.connect(self.abrir_menu_csv)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.btn_dicom)
        layout.addWidget(self.btn_jpg)
        layout.addWidget(self.btn_csv)

        self.setLayout(layout)

    def abrir_menu_dicom(self):
        self.menu_dicom = MenuDicom(self.modelo)
        self.menu_dicom.show()

    def abrir_menu_jpg(self):
        self.menu_jpg = MenuImagenesJPG(self.modelo)
        self.menu_jpg.show()

    def abrir_menu_csv(self):
        self.menu_csv = MenuSenales(self.modelo)
        self.menu_csv.show()

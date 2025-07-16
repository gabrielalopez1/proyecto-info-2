from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel, QTableView, QComboBox
import pandas as pd
from PyQt5.QtCore import QAbstractTableModel, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from modelo.procesador_csv import ProcesadorCSV
from modelo.modelo_datos import ModeloDatos
from modelo.pandas_model import PandasModel


class MenuCSV(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visualización de Datos CSV")
        self.procesador = ProcesadorCSV()
        self.modelo = ModeloDatos()  # ✅ Para registrar los archivos
        self.df = None
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
        self.btn_cargar = QPushButton("Cargar CSV")
        self.btn_cargar.clicked.connect(self.cargar_csv)

        self.combo_x = QComboBox()
        self.combo_y = QComboBox()

        self.btn_graficar = QPushButton("Graficar Dispersión")
        self.btn_graficar.clicked.connect(self.graficar_dispersion)

        self.tabla = QTableView()

        self.figura = Figure()
        self.canvas = FigureCanvas(self.figura)

        layout = QVBoxLayout()
        layout.addWidget(self.btn_cargar)
        layout.addWidget(QLabel("Columna X:"))
        layout.addWidget(self.combo_x)
        layout.addWidget(QLabel("Columna Y:"))
        layout.addWidget(self.combo_y)
        layout.addWidget(self.btn_graficar)
        layout.addWidget(QLabel("Datos CSV:"))
        layout.addWidget(self.tabla)
        layout.addWidget(QLabel("Gráfico de Dispersión:"))
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def cargar_csv(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Seleccionar CSV", "", "CSV Files (*.csv)")
        if ruta:
            self.df = self.procesador.cargar_csv(ruta)
            if self.df is not None:
                self.combo_x.clear()
                self.combo_y.clear()
                self.combo_x.addItems(self.df.columns)
                self.combo_y.addItems(self.df.columns)

                model = PandasModel(self.df)
                self.tabla.setModel(model)

                # ✅ Registrar el archivo
                nombre = ruta.split("/")[-1]
                self.modelo.registrar_archivo("CSV", nombre, ruta)
                print(f"✅ Archivo CSV registrado: {nombre}")

    def graficar_dispersion(self):
        if self.df is not None:
            col_x = self.combo_x.currentText()
            col_y = self.combo_y.currentText()
            if col_x and col_y:
                self.figura.clear()
                ax = self.figura.add_subplot(111)
                ax.scatter(self.df[col_x], self.df[col_y], color='blue')
                ax.set_title(f'Dispersión: {col_x} vs {col_y}')
                ax.set_xlabel(col_x)
                ax.set_ylabel(col_y)
                self.canvas.draw()

    



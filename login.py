from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from vista.menu_senales import MenuSenales
from vista.menu_principal import MenuPrincipal

class LoginWindow(QWidget):
    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador          # ✅ Controlador recibido desde main.py
        self.modelo = controlador.modelo        # ✅ Reutiliza el modelo del controlador

        self.setWindowTitle("Login BioApp")
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
        self.label_user = QLabel("Usuario:")
        self.input_user = QLineEdit()
        self.label_pass = QLabel("Contraseña:")
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.Password)

        self.btn_login = QPushButton("Ingresar")
        self.btn_login.clicked.connect(self.intentar_login)

        layout = QVBoxLayout()
        layout.addWidget(self.label_user)
        layout.addWidget(self.input_user)
        layout.addWidget(self.label_pass)
        layout.addWidget(self.input_pass)
        layout.addWidget(self.btn_login)

        self.setLayout(layout)

    def intentar_login(self):
        usuario = self.input_user.text()
        clave = self.input_pass.text()
        rol = self.controlador.verificar_login(usuario, clave)

        if rol == 'imagenes':
            self.hide()
            self.menu = MenuPrincipal(self.modelo)  # ✅ Menú completo para experto1
            self.menu.show()

        elif rol == 'senales':
            self.hide()
            self.menu = MenuSenales(self.modelo)    # ✅ Señales directo para experto2
            self.menu.show()

        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")
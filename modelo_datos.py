import sqlite3
from datetime import datetime

class ModeloDatos:
    def __init__(self):
        self.conn = sqlite3.connect('bioapp.db')
        self.cursor = self.conn.cursor()
        self.crear_tablas()

    def crear_tablas(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                rol TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS archivos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT,
                nombre TEXT,
                fecha TEXT,
                ruta TEXT
            )
        ''')

        self.conn.commit()

    def validar_usuario(self, usuario, clave):
        self.cursor.execute("SELECT rol FROM usuarios WHERE usuario=? AND clave=?", (usuario, clave))
        resultado = self.cursor.fetchone()
        return resultado[0] if resultado else None

    def registrar_archivo(self, tipo, nombre, ruta):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO archivos (tipo, nombre, fecha, ruta)
            VALUES (?, ?, ?, ?)
        ''', (tipo, nombre, fecha, ruta))
        self.conn.commit()


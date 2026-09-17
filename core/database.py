# core/database.py

import sqlite3
import hashlib

class DatabaseManager:
    def __init__(self, db_name="sistema_conjuntos.db"):
        self.db_name = db_name
        self.inicializar_db()

    def conectar(self):
        return sqlite3.connect(self.db_name)

    def inicializar_db(self):
        """Crea las tablas necesarias si no existen y un usuario administrador por defecto."""
        conexion = self.conectar()
        cursor = conexion.cursor()
        
        # Tabla de usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        
        # Tabla opcional para guardar historiales de conjuntos o operaciones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historial (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                operacion TEXT,
                resultado TEXT,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conexion.commit()

        # Insertar un usuario por defecto (admin / 1234) si no existe
        cursor.execute("SELECT * FROM usuarios WHERE username = ?", ("admin",))
        if not cursor.fetchone():
            # Contraseña hasheada por seguridad (opcional, pero buena práctica)
            pass_hash = hashlib.sha256("1234".encode()).hexdigest()
            cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", ("admin", pass_hash))
            conexion.commit()

        conexion.close()

    def verificar_usuario(self, username, password):
        """Verifica las credenciales consultando la base de datos."""
        conexion = self.conectar()
        cursor = conexion.cursor()
        
        pass_hash = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", (username, pass_hash))
        usuario = cursor.fetchone()
        
        conexion.close()
        return usuario is not None

    def registrar_historial(self, username, operacion, resultado):
        """Guarda una operación realizada en la base de datos."""
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuarios... (no, historial) VALUES (?, ?, ?)", (username, operacion, resultado)) # Ajustado abajo
        # Corrigiendo inserción en historial:
        cursor.execute("INSERT INTO historial (username, operacion, resultado) VALUES (?, ?, ?)", (username, operacion, resultado))
        conexion.commit()
        conexion.close()

    def registrar_usuario(self, username, password):
        """Registra un nuevo usuario en la base de datos."""
        conexion = self.conectar()
        cursor = conexion.cursor()
        try:
            pass_hash = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, pass_hash))
            conexion.commit()
            return True, "¡Usuario registrado con éxito!"
        except sqlite3.IntegrityError:
            return False, "❌ El nombre de usuario ya existe."
        except Exception as e:
            return False, f"❌ Error: {str(e)}"
        finally:
            conexion.close()
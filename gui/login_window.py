# gui/login_window.py

import customtkinter as ctk
from core.database import DatabaseManager

class LoginWindow(ctk.CTk):
    def __init__(self, on_success):
        super().__init__()
        self.on_success = on_success
        self.db = DatabaseManager()

        self.title("Acceso al Sistema - Alejandro Morales.")
        self.geometry("400x340")  # Aumentamos un poco la altura para el nuevo botón
        self.resizable(False, False)

        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

        self.setup_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_ui(self):
        ctk.CTkLabel(self, text="🔒 Portal de Acceso", font=("Arial", 20, "bold")).pack(pady=(25, 15))

        self.entry_user = ctk.CTkEntry(self, placeholder_text="Usuario", width=280, height=40)
        self.entry_user.pack(pady=8)

        self.entry_pass = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*", width=280, height=40)
        self.entry_pass.pack(pady=8)

        self.lbl_error = ctk.CTkLabel(self, text="", text_color="#ef4444", font=("Arial", 11))
        self.lbl_error.pack(pady=2)

        self.btn_login = ctk.CTkButton(self, text="Ingresar", width=280, height=38, fg_color="#1d4ed8", hover_color="#1e40af", command=self.verificar_credenciales)
        self.btn_login.pack(pady=5)

        # 🆕 Botón para abrir la ventana de registro rápido
        self.btn_registrar_modal = ctk.CTkButton(self, text="¿No tienes cuenta? Regístrate", width=280, height=32, fg_color="transparent", text_color="#3498db", hover_color="#242424", command=self.abrir_ventana_registro)
        self.btn_registrar_modal.pack(pady=5)

    def verificar_credenciales(self):
        usuario = self.entry_user.get().strip()
        contrasena = self.entry_pass.get().strip()

        if not usuario or not contrasena:
            self.lbl_error.configure(text="Por favor, ingrese usuario y contraseña.")
            return

        if self.db.verificar_usuario(usuario, contrasena):
            self.destroy()
            self.on_success()
        else:
            self.lbl_error.configure(text="❌ Usuario o contraseña incorrectos.")

    def abrir_ventana_registro(self):
        """Abre una sub-ventana rápida para registrar un nuevo usuario."""
        ventana_reg = ctk.CTkToplevel(self)
        ventana_reg.title("Registro de Nuevo Usuario")
        ventana_reg.geometry("350x280")
        ventana_reg.resizable(False, False)
        ventana_reg.grab_set() # Bloquea la ventana de atrás mientras está abierta

        ctk.CTkLabel(ventana_reg, text="📝 Crear Cuenta", font=("Arial", 16, "bold")).pack(pady=(20, 15))

        entry_nuevo_user = ctk.CTkEntry(ventana_reg, placeholder_text="Nuevo Usuario", width=250, height=35)
        entry_nuevo_user.pack(pady=8)

        entry_nuevo_pass = ctk.CTkEntry(ventana_reg, placeholder_text="Nueva Contraseña", show="*", width=250, height=35)
        entry_nuevo_pass.pack(pady=8)

        lbl_reg_msg = ctk.CTkLabel(ventana_reg, text="", font=("Arial", 11))
        lbl_reg_msg.pack(pady=2)

        def ejecutar_registro():
            u = entry_nuevo_user.get().strip()
            p = entry_nuevo_pass.get().strip()
            if not u or not p:
                lbl_reg_msg.configure(text="Rellene todos los campos.", text_color="#ef4444")
                return
            
            exito, mensaje = self.db.registrar_usuario(u, p)
            if exito:
                lbl_reg_msg.configure(text=mensaje, text_color="#2ecc71")
                self.after(1200, ventana_reg.destroy) # Cierra la ventanita tras 1.2 segundos
            else:
                lbl_reg_msg.configure(text=mensaje, text_color="#ef4444")

        btn_guardar = ctk.CTkButton(ventana_reg, text="Registrarse", width=250, height=35, fg_color="#27ae60", hover_color="#219653", command=ejecutar_registro)
        btn_guardar.pack(pady=10)
    
    def on_closing(self):
        import sys
        self.destroy()
        sys.exit(0)
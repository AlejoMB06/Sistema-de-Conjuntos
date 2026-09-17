# main.py

from gui.login_window import LoginWindow
from gui.main_window import MainWindow

def iniciar_app():
    # Esta función se ejecuta al pasar el login exitosamente
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    # Arrancamos mostrando la ventana de Login
    login = LoginWindow(on_success=iniciar_app)
    login.mainloop()
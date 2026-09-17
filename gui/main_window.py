# gui/main_window.py

import customtkinter as ctk
from models.set_model import Conjunto, ConjuntoUniversal
from core.validator import SetValidator
from core.set_engine import SetEngine
from core.random_generator import RandomSetGenerator
from gui.venn_visualizer import VennVisualizer
from core.evaluator import SetEvaluator

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Operaciones con Conjuntos - Alejandro Morales")
        self.geometry("1150x780")

        self.universal = None
        self.subconjuntos = {}

        self.setup_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_ui(self):
        self.frame_izq = ctk.CTkScrollableFrame(self, width=460, corner_radius=0)
        self.frame_izq.pack(side="left", fill="both", expand=False, padx=10, pady=10)

        self.frame_der = ctk.CTkFrame(self, corner_radius=10)
        self.frame_der.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # --- SECCIÓN DE ENTRADAS ---
        ctk.CTkLabel(self.frame_izq, text="Configuración de Conjuntos", font=("Arial", 16, "bold")).pack(pady=10)

        ctk.CTkLabel(self.frame_izq, text="Conjunto Universal (U) [ej: 1,2,3,4,a,b]:", anchor="w").pack(fill="x", padx=5)
        self.entry_u = ctk.CTkEntry(self.frame_izq, placeholder_text="1, 2, 3, 4, 5, 6, 7, 8")
        self.entry_u.pack(fill="x", padx=5, pady=5)

        self.entries_sub = {}
        for nombre in ["A", "B", "C", "D"]:
            ctk.CTkLabel(self.frame_izq, text=f"Subconjunto {nombre}:", anchor="w").pack(fill="x", padx=5)
            entry = ctk.CTkEntry(self.frame_izq, placeholder_text=f"Elementos de {nombre}")
            entry.pack(fill="x", padx=5, pady=5)
            self.entries_sub[nombre] = entry

        self.btn_cargar = ctk.CTkButton(self.frame_izq, text="1. Cargar y Validar Conjuntos", fg_color="#2b8a3e", hover_color="#237032", command=self.cargar_y_validar)
        self.btn_cargar.pack(fill="x", padx=5, pady=15)

        self.btn_random = ctk.CTkButton(self.frame_izq, text="🎲 Modo Aleatorio Automático", fg_color="#d97706", hover_color="#b45309", command=self.cargar_modo_aleatorio)
        self.btn_random.pack(fill="x", padx=5, pady=5)

        # --- NUEVO BOTÓN: LIMPIAR TODO ---
        self.btn_limpiar = ctk.CTkButton(self.frame_izq, text="🗑️ Limpiar Todo / Reiniciar", fg_color="#c0392b", hover_color="#962d22", command=self.limpiar_todo)
        self.btn_limpiar.pack(fill="x", padx=5, pady=(5, 15))

        # --- SECCIÓN DE OPERACIÓN MANUAL PERSONALIZADA ---
        self.frame_manual = ctk.CTkFrame(self.frame_izq, fg_color="#242424", corner_radius=8)
        self.frame_manual.pack(fill="x", padx=5, pady=10)

        ctk.CTkLabel(self.frame_manual, text="🧮 Operación Manual", font=("Arial", 13, "bold")).pack(anchor="w", padx=10, pady=(8, 2))
        
        self.entry_expresion = ctk.CTkEntry(self.frame_manual, placeholder_text="Ej: (A | B) & C  (Usa |, &, -)", height=32)
        self.entry_expresion.pack(fill="x", padx=10, pady=5)

        self.btn_calcular_manual = ctk.CTkButton(self.frame_manual, text="Calcular Expresión Manual", fg_color="#3498db", hover_color="#2980b9", command=self.ejecutar_calculo_manual, height=30)
        self.btn_calcular_manual.pack(fill="x", padx=10, pady=(5, 10))

        # --- SECCIÓN DE OPERACIONES MULTI-CONJUNTO ---
        ctk.CTkLabel(self.frame_izq, text="Selección de Operaciones", font=("Arial", 16, "bold")).pack(pady=(10, 10))

        self.op_var = ctk.StringVar(value="Unión Multi-conjunto (A ∪ B ∪ C ∪ ...)")
        operaciones = [
            "Unión Multi-conjunto (A ∪ B ∪ C ∪ ...)", 
            "Intersección Multi-conjunto (A ∩ B ∩ C ∩ ...)", 
            "Diferencia (A - B)", 
            "Diferencia Simétrica (A Δ B)", 
            "Complemento (A')"
        ]
        self.menu_ops = ctk.CTkOptionMenu(self.frame_izq, values=operaciones, variable=self.op_var, command=self.cambiar_modo_operacion)
        self.menu_ops.pack(fill="x", padx=5, pady=5)

        self.frame_multi = ctk.CTkFrame(self.frame_izq)
        self.frame_multi.pack(fill="x", padx=5, pady=10)
        
        ctk.CTkLabel(self.frame_multi, text="Seleccione conjuntos a operar:", font=("Arial", 12, "bold")).pack(anchor="w", padx=5, pady=5)
        
        self.checkboxes_sub = {}
        self.check_vars = {}
        for nombre in ["A", "B", "C", "D"]:
            var = ctk.BooleanVar(value=True if nombre in ["A", "B"] else False)
            chk = ctk.CTkCheckBox(self.frame_multi, text=f"Conjunto {nombre}", variable=var)
            chk.pack(anchor="w", padx=10, pady=2)
            self.checkboxes_sub[nombre] = chk
            self.check_vars[nombre] = var

        self.frame_binario = ctk.CTkFrame(self.frame_izq)
        
        ctk.CTkLabel(self.frame_binario, text="Conjunto 1:").grid(row=0, column=0, padx=5, pady=5)
        self.c1_var = ctk.StringVar(value="A")
        self.menu_c1 = ctk.CTkOptionMenu(self.frame_binario, values=["A", "B", "C", "D"], variable=self.c1_var, width=80)
        self.menu_c1.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(self.frame_binario, text="Conjunto 2:").grid(row=0, column=2, padx=5, pady=5)
        self.c2_var = ctk.StringVar(value="B")
        self.menu_c2 = ctk.CTkOptionMenu(self.frame_binario, values=["A", "B", "C", "D"], variable=self.c2_var, width=80)
        self.menu_c2.grid(row=0, column=3, padx=5, pady=5)

        self.btn_calcular = ctk.CTkButton(self.frame_izq, text="2. Ejecutar Operación", fg_color="#1d4ed8", hover_color="#1e40af", command=self.ejecutar_operacion)
        self.btn_calcular.pack(fill="x", padx=5, pady=15)

        # --- PANEL DERECHO ---
        ctk.CTkLabel(self.frame_der, text="Resultados y Análisis", font=("Arial", 18, "bold")).pack(pady=10)
        
        self.text_resultado = ctk.CTkTextbox(self.frame_der, height=120, font=("Consolas", 12))
        self.text_resultado.pack(fill="x", padx=10, pady=5)
        self.text_resultado.insert("0.0", "Bienvenido. Ingrese sus conjuntos o use el modo aleatorio para comenzar.")

        self.frame_venn = ctk.CTkFrame(self.frame_der, fg_color="#242424")
        self.frame_venn.pack(fill="both", expand=True, padx=10, pady=10)

    def cambiar_modo_operacion(self, eleccion):
        if "Multi-conjunto" in eleccion:
            self.frame_binario.pack_forget()
            self.frame_multi.pack(fill="x", padx=5, pady=10)
        else:
            self.frame_multi.pack_forget()
            self.frame_binario.pack(fill="x", padx=5, pady=10)

    def limpiar_todo(self):
        """Borra todos los campos de entrada, reinicia las variables y limpia resultados y gráficos."""
        self.universal = None
        self.subconjuntos = {}

        # Limpiar campo de U
        self.entry_u.delete(0, "end")

        # Limpiar campos de subconjuntos A, B, C, D
        for entry in self.entries_sub.values():
            entry.delete(0, "end")

        # Limpiar campo de expresión manual
        self.entry_expresion.delete(0, "end")

        # Restaurar texto de bienvenida en la consola de resultados
        self.mostrar_resultado("🧹 Sistema reiniciado. Ingrese nuevos conjuntos o use el modo aleatorio.")

        # Limpiar el frame del diagrama de Venn destruyendo sus widgets hijos actuales
        for widget in self.frame_venn.winfo_children():
            widget.destroy()

    def cargar_y_validar(self):
        try:
            elems_u = SetValidator.parsear_entrada(self.entry_u.get())
            self.universal = ConjuntoUniversal(elems_u)

            self.subconjuntos = {}
            for nombre, entry in self.entries_sub.items():
                elems = SetValidator.parsear_entrada(entry.get())
                self.subconjuntos[nombre] = Conjunto(nombre, elems)

            valido, mensaje = SetValidator.validar_subconjuntos(self.universal, self.subconjuntos)
            if not valido:
                self.mostrar_resultado(f"❌ ERROR DE VALIDACIÓN:\n{mensaje}")
                return

            info = f"✅ ¡Validación Exitosa (Elementos dentro de U)!\n{self.universal}\n"
            for nombre, sub in self.subconjuntos.items():
                info += f"{sub} (Tipo: {sub.obtener_tipo()})\n"
            
            self.mostrar_resultado(info)

        except Exception as e:
            self.mostrar_resultado(f"❌ Error al procesar los datos: {str(e)}")

    def cargar_modo_aleatorio(self):
        self.universal, self.subconjuntos, sugerencia = RandomSetGenerator.generar_sistema_aleatorio()
        
        self.entry_u.delete(0, "end")
        self.entry_u.insert(0, ", ".join(str(e) for e in self.universal.elementos))

        for nombre, sub in self.subconjuntos.items():
            self.entries_sub[nombre].delete(0, "end")
            self.entries_sub[nombre].insert(0, ", ".join(str(e) for e in sub.elementos))

        info = f"🎲 [MODO ALEATORIO ACTIVADO]\n{self.universal}\n"
        for nombre, sub in self.subconjuntos.items():
            info += f"{sub} (Tipo: {sub.obtener_tipo()})\n"
        info += f"\nSugerencia de prueba: {sugerencia}"
        
        self.mostrar_resultado(info)

    def ejecutar_operacion(self):
        if not self.universal or not self.subconjuntos:
            self.mostrar_resultado("❌ Primero debe cargar y validar los conjuntos.")
            return

        opcion = self.op_var.get()

        try:
            if "Multi-conjunto" in opcion:
                conjuntos_activos = [self.subconjuntos[n] for n, var in self.check_vars.items() if var.get()]
                if len(conjuntos_activos) < 2:
                    self.mostrar_resultado("❌ Debe seleccionar al menos 2 conjuntos para realizar una operación multi-conjunto.")
                    return
                
                nombres_sel = " ∪ ".join([c.nombre for c in conjuntos_activos]) if "Unión" in opcion else " ∩ ".join([c.nombre for c in conjuntos_activos])
                
                if "Unión" in opcion:
                    elems_res = SetEngine.union_multi(conjuntos_activos)
                else:
                    elems_res = SetEngine.interseccion_multi(conjuntos_activos)
                
                res = Conjunto(f"({nombres_sel})", elems_res)
                
                detalle = f"📌 Operación: {opcion}\n"
                detalle += f"Resultado: {res}\n"
                detalle += f"Cardinalidad: {res.cardinalidad()}\n"
                detalle += f"Clasificación del Conjunto: {res.obtener_tipo()}"
                
                self.mostrar_resultado(detalle)
                VennVisualizer.generar_diagrama_venn(self.frame_venn, conjuntos_activos)

            else:
                c1_nombre = self.c1_var.get()
                c2_nombre = self.c2_var.get()
                c1 = self.subconjuntos.get(c1_nombre)
                c2 = self.subconjuntos.get(c2_nombre)

                if "Diferencia Simétrica" in opcion:
                    res = SetEngine.diferencia_simetrica(c1, c2)
                elif "Diferencia" in opcion:
                    res = SetEngine.diferencia(c1, c2)
                elif "Complemento" in opcion:
                    res = SetEngine.complemento(c1, self.universal)
                else:
                    return

                detalle = f"📌 Operación: {opcion}\n"
                detalle += f"Resultado: {res}\n"
                detalle += f"Cardinalidad: {res.cardinalidad()}\n"
                detalle += f"Clasificación del Conjunto: {res.obtener_tipo()}"
                
                self.mostrar_resultado(detalle)
                VennVisualizer.generar_diagrama_venn(self.frame_venn, [c1, c2])

        except Exception as e:
            self.mostrar_resultado(f"❌ Error al calcular la operación: {str(e)}")

    def ejecutar_calculo_manual(self):
        if not self.universal or not self.subconjuntos:
            self.mostrar_resultado("❌ Primero debe cargar y validar los conjuntos antes de evaluar una expresión manual.")
            return

        expresion = self.entry_expresion.get()
        if not expresion.strip():
            self.mostrar_resultado("❌ La expresión manual está vacía.")
            return

        try:
            conjuntos_dict = {nombre: sub for nombre, sub in self.subconjuntos.items()}
            
            resultado_elementos = SetEvaluator.evaluar_expresion(expresion, conjuntos_dict)
            res = Conjunto(f"Expresión: {expresion}", resultado_elementos)

            detalle = f"🧮 Operación Manual: {expresion}\n"
            detalle += f"Resultado: {res}\n"
            detalle += f"Cardinalidad: {res.cardinalidad()}\n"
            detalle += f"Clasificación del Conjunto: {res.obtener_tipo()}"
            
            self.mostrar_resultado(detalle)

            activos_en_exp = [sub for nombre, sub in self.subconjuntos.items() if nombre in expresion]
            if activos_en_exp:
                VennVisualizer.generar_diagrama_venn(self.frame_venn, activos_en_exp)

        except Exception as e:
            self.mostrar_resultado(f"❌ Error al evaluar la expresión '{expresion}': {str(e)}")

    def mostrar_resultado(self, texto):
        self.text_resultado.delete("0.0", "end")
        self.text_resultado.insert("0.0", texto)

    def on_closing(self):
        import sys
        self.destroy()
        sys.exit(0)
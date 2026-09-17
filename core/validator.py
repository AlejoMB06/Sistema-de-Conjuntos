# core/validator.py

from models.set_model import Conjunto, ConjuntoUniversal

class SetValidator:
    @staticmethod
    def parsear_entrada(texto: str) -> set:
        """
        Toma una cadena de texto separada por comas, limpia espacios
        y convierte los valores numéricos automáticamente si es posible.
        """
        if not texto or not texto.strip():
            return set()
        
        elementos_crudoss = texto.split(",")
        elementos_limpios = set()
        
        for item in elementos_crudoss:
            item_limpio = item.strip()
            if not item_limpio:
                continue
            
            # Intentar convertir a entero o flotante si aplica, sino dejar como string
            try:
                if "." in item_limpio:
                    val = float(item_limpio)
                else:
                    val = int(item_limpio)
                elementos_limpios.add(val)
            except ValueError:
                # Si no es número, se queda como cadena de texto
                elementos_limpios.add(item_limpio)
                
        return elementos_limpios

    @staticmethod
    def validar_subconjuntos(universal: ConjuntoUniversal, subconjuntos: dict) -> tuple[bool, str]:
        """
        Valida que cada subconjunto cumpla estrictamente con pertenecer al Universal.
        Retorna (True, "") si todo está bien, o (False, mensaje_error) si falla.
        """
        for nombre, sub in subconjuntos.items():
            if not universal.validar_pertenencia(sub):
                invalidos = sub.elementos - universal.elementos
                return False, f"El subconjunto '{nombre}' contiene elementos no permitidos en U: {invalidos}"
        return True, "Validación exitosa"
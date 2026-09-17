# core/set_operations.py (o tu archivo de lógica de conjuntos)

class SetEvaluator:
    @staticmethod
    def evaluar_expresion(expresion_texto, conjuntos_dict):
        """
        Toma una cadena de texto con la operación (ej: "(A | B) & C") 
        y un diccionario con los conjuntos activos {'A': obj_A, 'B': obj_B, ...},
        y devuelve el conjunto resultante de elementos.
        """
        # 1. Limpiar espacios en blanco alrededor de la expresión
        expresion = expresion_texto.strip()
        
        # 2. Reemplazar símbolos amigables para que el usuario pueda escribir de forma natural
        # Acepta tanto notación matemática/lógica como operadores directos de Python
        expresion = expresion.replace(' U ', ' | ').replace('unión', '|').replace('UNION', '|')
        expresion = expresion.replace(' ∩ ', ' & ').replace('intersección', '&').replace('INTERSECCION', '&')
        
        # 3. Construir un diccionario seguro únicamente con los conjuntos y sus elementos (sets de Python)
        # Esto mapea el nombre de la letra (ej: 'A') directamente con su contenido real ({1, 2, 3})
        entorno_seguro = {nombre: c.elementos for nombre, c in conjuntos_dict.items()}
        
        try:
            # 4. eval() procesa la expresión matemática de forma dinámica utilizando los sets del entorno.
            # "__builtins__": None se usa por seguridad estricta para impedir que se ejecuten comandos maliciosos.
            resultado_elementos = eval(expresion, {"__builtins__": None}, entorno_seguro)
            
            # Asegurarse de retornar un objeto tipo set de Python con el resultado final
            return set(resultado_elementos)
            
        except Exception as e:
            # Si el usuario escribe una letra que no existe o comete un error de sintaxis,
            # atrapamos el error para mostrarlo amigablemente en la interfaz.
            raise ValueError(f"Error en la sintaxis o conjuntos inválidos: {e}")
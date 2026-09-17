# core/random_generator.py

import random
from models.set_model import Conjunto, ConjuntoUniversal

class RandomSetGenerator:
    @staticmethod
    def generar_sistema_aleatorio() -> tuple[ConjuntoUniversal, dict, str]:
        """
        Genera un conjunto universal aleatorio de números o letras,
        crea 4 subconjuntos válidos (A, B, C, D) y sugiere una operación aleatoria.
        """
        # Definir un universo base aleatorio (por ejemplo, números del 1 al 15 o letras)
        tipo_universo = random.choice(["numeros", "letras"])
        
        if tipo_universo == "numeros":
            elementos_base = random.sample(range(1, 20), k=random.randint(8, 12))
        else:
            pool_letras = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
            elementos_base = random.sample(pool_letras, k=random.randint(8, 12))

        universal = ConjuntoUniversal(elementos_base)
        
        # Generar 4 subconjuntos garantizando que sean subconjuntos de U
        nombres_sub = ["A", "B", "C", "D"]
        subconjuntos = {}
        
        lista_elementos = list(universal.elementos)
        for nombre in nombres_sub:
            # Seleccionar una cantidad aleatoria de elementos del universal para este subconjunto
            k_elementos = random.randint(2, max(2, len(lista_elementos) - 1))
            elementos_sub = random.sample(lista_elementos, k=k_elementos)
            subconjuntos[nombre] = Conjunto(nombre, elementos_sub)

        # Seleccionar operación aleatoria de ejemplo
        opciones_ops = [
            f"Unión: {nombres_sub[0]} ∪ {nombres_sub[1]}",
            f"Intersección: {nombres_sub[1]} ∩ {nombres_sub[2]}",
            f"Diferencia: {nombres_sub[0]} - {nombres_sub[3]}",
            f"Diferencia Simétrica: {nombres_sub[2]} Δ {nombres_sub[3]}",
            f"Complemento: {nombres_sub[0]}'"
        ]
        operacion_sugerida = random.choice(opciones_ops)

        return universal, subconjuntos, operacion_sugerida
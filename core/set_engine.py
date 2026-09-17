# core/set_engine.py

from models.set_model import Conjunto, ConjuntoUniversal

class SetEngine:
    @staticmethod
    def union(conjunto1: Conjunto, conjunto2: Conjunto) -> Conjunto:
        resultado_elementos = conjunto1.elementos.union(conjunto2.elementos)
        return Conjunto(f"({conjunto1.nombre} ∪ {conjunto2.nombre})", resultado_elementos)

    @staticmethod
    def interseccion(conjunto1: Conjunto, conjunto2: Conjunto) -> Conjunto:
        resultado_elementos = conjunto1.elementos.intersection(conjunto2.elementos)
        return Conjunto(f"({conjunto1.nombre} ∩ {conjunto2.nombre})", resultado_elementos)

    @staticmethod
    def diferencia(conjunto1: Conjunto, conjunto2: Conjunto) -> Conjunto:
        resultado_elementos = conjunto1.elementos.difference(conjunto2.elementos)
        return Conjunto(f"({conjunto1.nombre} - {conjunto2.nombre})", resultado_elementos)

    @staticmethod
    def diferencia_simetrica(conjunto1: Conjunto, conjunto2: Conjunto) -> Conjunto:
        resultado_elementos = conjunto1.elementos.symmetric_difference(conjunto2.elementos)
        return Conjunto(f"({conjunto1.nombre} Δ {conjunto2.nombre})", resultado_elementos)

    @staticmethod
    def complemento(conjunto: Conjunto, universal: ConjuntoUniversal) -> Conjunto:
        resultado_elementos = universal.elementos.difference(conjunto.elementos)
        return Conjunto(f"({conjunto.nombre}')", resultado_elementos)

    @staticmethod
    def union_multi(conjuntos: list[Conjunto]) -> set:
        if not conjuntos:
            return set()
        resultado = set(conjuntos[0].elementos)
        for c in conjuntos[1:]:
            resultado = resultado.union(c.elementos)
        return resultado

    @staticmethod
    def interseccion_multi(conjuntos: list[Conjunto]) -> set:
        if not conjuntos:
            return set()
        resultado = set(conjuntos[0].elementos)
        for c in conjuntos[1:]:
            resultado = resultado.intersection(c.elementos)
        return resultado
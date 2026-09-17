# models/set_model.py

class Conjunto:
    """
    Representa un conjunto matemático individual (subconjunto o universal)
    almacenando sus elementos de forma única y ordenada.
    """
    def __init__(self, nombre: str, elementos=None):
        self.nombre = nombre.upper()
        # Usamos un set de Python para garantizar elementos únicos (O(1))
        # y luego los guardamos ordenados o en formato nativo.
        self._elementos = set(elementos) if elementos else set()

    @property
    def elementos(self):
        return self._elementos

    @elementos.setter
    def elementos(self, nuevos_elementos):
        self._elementos = set(nuevos_elementos)

    def agregar_elemento(self, elemento):
        self._elementos.add(elemento)

    def eliminar_elemento(self, elemento):
        if elemento in self._elementos:
            self._elementos.remove(elemento)

    def cardinalidad(self) -> int:
        return len(self._elementos)

    def obtener_tipo(self) -> str:
        """
        Clasifica automáticamente el tipo de conjunto según su cardinalidad.
        """
        card = self.cardinalidad()
        if card == 0:
            return "Vacío"
        elif card == 1:
            return "Unitario"
        else:
            return "Finito"

    def __str__(self):
        # Muestra el conjunto en formato matemático clásico: A = {1, 2, 3}
        elementos_ordenados = sorted(list(self._elementos), key=str)
        return f"{self.nombre} = {{{', '.join(str(e) for e in elementos_ordenados)}}}"


class ConjuntoUniversal(Conjunto):
    """
    Hereda de Conjunto para actuar como el marco de referencia absoluto
    contra el cual se validarán los subconjuntos y se calcularán complementos.
    """
    def __init__(self, elementos=None):
        super().__init__("U", elementos)

    def validar_pertenencia(self, subconjunto: Conjunto) -> bool:
        """
        Verifica estrictamente que todos los elementos del subconjunto
        existan dentro del Conjunto Universal.
        """
        return subconjunto.elementos.issubset(self._elementos)
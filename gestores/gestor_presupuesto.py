class GestorPresupuesto:
    def __init__(self):
        self._limites: dict = {}
        self._ingresos_semanales: dict = {}
        self._categorias: list = []

    @property
    def limites(self):
        return self._limites

    @property
    def ingresos_semanales(self):
        return self._ingresos_semanales

    @property
    def categorias(self):
        return self._categorias

    def agregar_limite(self, categoria: str, monto: float) -> None:
        self._limites[categoria] = monto
        if categoria not in self._categorias:
            self._categorias.append(categoria)

    def obtener_limite(self, categoria: str) -> float:
        return self._limites.get(categoria, 0.0)

    def agregar_categoria(self, nombre: str) -> None:
        if nombre not in self._categorias:
            self._categorias.append(nombre)

    def calcular_gasto_categoria(self, transacciones: list, categoria: str) -> float:
        from modelos.gasto import Gasto
        return sum(t.monto for t in transacciones
                   if isinstance(t, Gasto) and t.categoria == categoria)

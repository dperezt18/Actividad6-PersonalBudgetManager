import uuid


class Meta:
    def __init__(self, nombre: str, emoji: str, categoria: str, monto_objetivo: float,
                 fecha_limite: str, id: str = None, monto_actual: float = 0.0,
                 completada: bool = False):
        self._id = id or str(uuid.uuid4())[:8]
        self._nombre = nombre
        self._emoji = emoji
        self._categoria = categoria
        self._monto_objetivo = monto_objetivo
        self._monto_actual = monto_actual
        self._fecha_limite = fecha_limite
        self._completada = completada

    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @property
    def emoji(self):
        return self._emoji

    @property
    def categoria(self):
        return self._categoria

    @property
    def monto_objetivo(self):
        return self._monto_objetivo

    @property
    def monto_actual(self):
        return self._monto_actual

    @property
    def fecha_limite(self):
        return self._fecha_limite

    @property
    def completada(self):
        return self._completada

    def agregar_dinero(self, monto: float) -> None:
        self._monto_actual += monto
        if self._monto_actual >= self._monto_objetivo:
            self._completada = True

    def retirar_dinero(self, monto: float) -> None:
        self._monto_actual = max(0.0, self._monto_actual - monto)
        self._completada = self._monto_actual >= self._monto_objetivo

    def calcular_progreso(self) -> float:
        if self._monto_objetivo == 0:
            return 0.0
        return min(100.0, (self._monto_actual / self._monto_objetivo) * 100)

    def __str__(self) -> str:
        progreso = self.calcular_progreso()
        estado = "Completada" if self._completada else f"{progreso:.1f}%"
        return (f"{self._emoji} {self._nombre} | "
                f"${self._monto_actual:,.0f} / ${self._monto_objetivo:,.0f} | "
                f"{estado} | Limite: {self._fecha_limite}")

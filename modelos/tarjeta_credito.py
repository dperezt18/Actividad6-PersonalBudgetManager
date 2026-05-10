import uuid


class TarjetaCredito:
    def __init__(self, nombre: str, cupo_total: float, saldo_actual: float = 0.0,
                 pago_minimo: float = 0.0, pago_total: float = 0.0,
                 dia_corte: int = 1, dia_pago: int = 15, id: str = None):
        self._id = id or str(uuid.uuid4())[:8]
        self._nombre = nombre
        self._cupo_total = cupo_total
        self._saldo_actual = saldo_actual
        self._pago_minimo = pago_minimo
        self._pago_total = pago_total
        self._dia_corte = dia_corte
        self._dia_pago = dia_pago

    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @property
    def cupo_total(self):
        return self._cupo_total

    @property
    def saldo_actual(self):
        return self._saldo_actual

    @property
    def pago_minimo(self):
        return self._pago_minimo

    @property
    def pago_total(self):
        return self._pago_total

    @property
    def dia_corte(self):
        return self._dia_corte

    @property
    def dia_pago(self):
        return self._dia_pago

    def registrar_pago(self, monto: float) -> None:
        self._saldo_actual = max(0.0, self._saldo_actual - monto)

    def calcular_disponible(self) -> float:
        return self._cupo_total - self._saldo_actual

    def calcular_uso(self) -> float:
        if self._cupo_total == 0:
            return 0.0
        return (self._saldo_actual / self._cupo_total) * 100

    def __str__(self) -> str:
        return (f"Tarjeta: {self._nombre} | "
                f"Cupo: ${self._cupo_total:,.0f} | "
                f"Usado: ${self._saldo_actual:,.0f} ({self.calcular_uso():.1f}%) | "
                f"Disponible: ${self.calcular_disponible():,.0f}")

from modelos.transaccion import Transaccion


class Gasto(Transaccion):
    def __init__(self, monto: float, descripcion: str, categoria: str,
                 fecha: str = None, meta_id: str = None):
        super().__init__(monto, descripcion, categoria, fecha)
        self._meta_id = meta_id

    @property
    def meta_id(self):
        return self._meta_id

    def registrar(self) -> None:
        print(f"  [GASTO]   -${self._monto:,.0f}  |  {self._categoria}  |  {self._descripcion}")

    def verificar_limite(self, limite: float) -> bool:
        return self._monto <= limite

    def __str__(self) -> str:
        return f"Gasto   | {self._fecha} | {self._categoria:<18} | -${self._monto:>10,.0f} | {self._descripcion}"

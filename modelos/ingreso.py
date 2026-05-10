from modelos.transaccion import Transaccion


class Ingreso(Transaccion):
    def __init__(self, monto: float, descripcion: str, categoria: str,
                 fecha: str = None, meta_id: str = None):
        super().__init__(monto, descripcion, categoria, fecha)
        self._meta_id = meta_id

    @property
    def meta_id(self):
        return self._meta_id

    def registrar(self) -> None:
        print(f"  [INGRESO] +${self._monto:,.0f}  |  {self._categoria}  |  {self._descripcion}")

    def __str__(self) -> str:
        return f"Ingreso | {self._fecha} | {self._categoria:<18} | +${self._monto:>10,.0f} | {self._descripcion}"

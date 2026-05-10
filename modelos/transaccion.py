from abc import ABC, abstractmethod
import uuid
from datetime import datetime


class Transaccion(ABC):
    def __init__(self, monto: float, descripcion: str, categoria: str, fecha: str = None):
        self._id = str(uuid.uuid4())[:8]
        self._monto = monto
        self._descripcion = descripcion
        self._categoria = categoria
        self._fecha = fecha or datetime.now().strftime("%Y-%m-%d")

    @property
    def id(self):
        return self._id

    @property
    def monto(self):
        return self._monto

    @property
    def descripcion(self):
        return self._descripcion

    @property
    def categoria(self):
        return self._categoria

    @property
    def fecha(self):
        return self._fecha

    @abstractmethod
    def registrar(self) -> None:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

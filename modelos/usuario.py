import uuid
import hashlib
from datetime import datetime


class Usuario:
    def __init__(self, nombre: str, username: str, password: str,
                 fecha_creacion: str = None, id: str = None):
        self._id = id or str(uuid.uuid4())[:8]
        self._nombre = nombre
        self._username = username
        self._password = password if self._ya_hasheado(password) else self._hash(password)
        self._fecha_creacion = fecha_creacion or datetime.now().strftime("%Y-%m-%d")

    def _hash(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def _ya_hasheado(self, password: str) -> bool:
        return len(password) == 64 and all(c in "0123456789abcdef" for c in password)

    def autenticar(self, password: str) -> bool:
        return self._password == self._hash(password)

    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    def __str__(self) -> str:
        return f"Usuario: {self._nombre} (@{self._username}) — desde {self._fecha_creacion}"

import os
from modelos.usuario import Usuario
from modelos.ingreso import Ingreso
from modelos.gasto import Gasto
from modelos.meta import Meta
from modelos.tarjeta_credito import TarjetaCredito


class GestorArchivos:
    def __init__(self, ruta_base: str = "data"):
        self._ruta_base = ruta_base
        os.makedirs(ruta_base, exist_ok=True)

    @property
    def ruta_base(self):
        return self._ruta_base

    def _ruta(self, nombre: str) -> str:
        return os.path.join(self._ruta_base, nombre)

    # ── Usuario ──────────────────────────────────────────────────────────────

    def guardar_usuario(self, usuario: Usuario) -> None:
        with open(self._ruta("usuario.txt"), "w", encoding="utf-8") as f:
            f.write(f"{usuario.id}|{usuario.nombre}|{usuario.username}|"
                    f"{usuario.password}|{usuario.fecha_creacion}\n")

    def cargar_usuario(self, username: str) -> Usuario | None:
        ruta = self._ruta("usuario.txt")
        if not os.path.exists(ruta):
            return None
        with open(ruta, "r", encoding="utf-8") as f:
            for linea in f:
                p = linea.strip().split("|")
                if len(p) == 5 and p[2] == username:
                    return Usuario(p[1], p[2], p[3], p[4], p[0])
        return None

    # ── Transacciones ────────────────────────────────────────────────────────

    def guardar_transacciones(self, transacciones: list) -> None:
        with open(self._ruta("transacciones.txt"), "w", encoding="utf-8") as f:
            for t in transacciones:
                tipo = "I" if isinstance(t, Ingreso) else "G"
                f.write(f"{tipo}|{t.id}|{t.monto}|{t.descripcion}|"
                        f"{t.categoria}|{t.fecha}|{t.meta_id or ''}\n")

    def cargar_transacciones(self) -> list:
        ruta = self._ruta("transacciones.txt")
        if not os.path.exists(ruta):
            return []
        transacciones = []
        with open(ruta, "r", encoding="utf-8") as f:
            for linea in f:
                p = linea.strip().split("|")
                if len(p) < 7:
                    continue
                tipo, id_, monto, desc, cat, fecha, meta_id = p
                meta_id = meta_id or None
                obj = (Ingreso(float(monto), desc, cat, fecha, meta_id)
                       if tipo == "I"
                       else Gasto(float(monto), desc, cat, fecha, meta_id))
                obj._id = id_
                transacciones.append(obj)
        return transacciones

    # ── Metas ────────────────────────────────────────────────────────────────

    def guardar_metas(self, metas: list) -> None:
        with open(self._ruta("metas.txt"), "w", encoding="utf-8") as f:
            for m in metas:
                f.write(f"{m.id}|{m.nombre}|{m.emoji}|{m.categoria}|"
                        f"{m.monto_objetivo}|{m.monto_actual}|"
                        f"{m.fecha_limite}|{int(m.completada)}\n")

    def cargar_metas(self) -> list:
        ruta = self._ruta("metas.txt")
        if not os.path.exists(ruta):
            return []
        metas = []
        with open(ruta, "r", encoding="utf-8") as f:
            for linea in f:
                p = linea.strip().split("|")
                if len(p) < 8:
                    continue
                metas.append(Meta(
                    nombre=p[1], emoji=p[2], categoria=p[3],
                    monto_objetivo=float(p[4]), fecha_limite=p[6],
                    id=p[0], monto_actual=float(p[5]),
                    completada=bool(int(p[7]))
                ))
        return metas

    # ── Tarjetas ─────────────────────────────────────────────────────────────

    def guardar_tarjetas(self, tarjetas: list) -> None:
        with open(self._ruta("tarjetas.txt"), "w", encoding="utf-8") as f:
            for t in tarjetas:
                f.write(f"{t.id}|{t.nombre}|{t.cupo_total}|{t.saldo_actual}|"
                        f"{t.pago_minimo}|{t.pago_total}|{t.dia_corte}|{t.dia_pago}\n")

    def cargar_tarjetas(self) -> list:
        ruta = self._ruta("tarjetas.txt")
        if not os.path.exists(ruta):
            return []
        tarjetas = []
        with open(ruta, "r", encoding="utf-8") as f:
            for linea in f:
                p = linea.strip().split("|")
                if len(p) < 8:
                    continue
                tarjetas.append(TarjetaCredito(
                    nombre=p[1], cupo_total=float(p[2]),
                    saldo_actual=float(p[3]), pago_minimo=float(p[4]),
                    pago_total=float(p[5]), dia_corte=int(p[6]),
                    dia_pago=int(p[7]), id=p[0]
                ))
        return tarjetas

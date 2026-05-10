import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modelos.usuario import Usuario
from modelos.ingreso import Ingreso
from modelos.gasto import Gasto
from modelos.meta import Meta
from modelos.tarjeta_credito import TarjetaCredito
from gestores.gestor_presupuesto import GestorPresupuesto
from gestores.gestor_archivos import GestorArchivos

LINEA = "─" * 52


def encabezado(titulo: str):
    print(f"\n{LINEA}")
    print(f"  {titulo}")
    print(LINEA)


def menu_principal() -> str:
    encabezado("PersonalBudgetManager")
    print("  1. Registrar ingreso")
    print("  2. Registrar gasto")
    print("  3. Ver transacciones")
    print("  4. Metas de ahorro")
    print("  5. Tarjetas de credito")
    print("  6. Resumen de presupuesto")
    print("  0. Salir")
    print(LINEA)
    return input("  Opcion: ").strip()


def registrar_ingreso(transacciones, gestor_archivos, gestor_presupuesto):
    encabezado("Nuevo Ingreso")
    monto = float(input("  Monto: $"))
    descripcion = input("  Descripcion: ")
    print(f"  Categorias disponibles: {gestor_presupuesto.categorias or ['Trabajo','Extra','Otros']}")
    categoria = input("  Categoria: ")
    ingreso = Ingreso(monto, descripcion, categoria)
    ingreso.registrar()
    transacciones.append(ingreso)
    gestor_archivos.guardar_transacciones(transacciones)
    print("  Guardado correctamente.")


def registrar_gasto(transacciones, gestor_archivos, gestor_presupuesto):
    encabezado("Nuevo Gasto")
    monto = float(input("  Monto: $"))
    descripcion = input("  Descripcion: ")
    print(f"  Categorias disponibles: {gestor_presupuesto.categorias or ['Alimentacion','Transporte','Otros']}")
    categoria = input("  Categoria: ")
    gasto = Gasto(monto, descripcion, categoria)
    limite = gestor_presupuesto.obtener_limite(categoria)
    if limite > 0 and not gasto.verificar_limite(limite):
        print(f"  ALERTA: Este gasto (${monto:,.0f}) supera el limite de ${limite:,.0f} para '{categoria}'")
    gasto.registrar()
    transacciones.append(gasto)
    gestor_archivos.guardar_transacciones(transacciones)
    print("  Guardado correctamente.")


def ver_transacciones(transacciones):
    encabezado("Historial de Transacciones")
    if not transacciones:
        print("  Sin transacciones registradas.")
        return
    total_ingresos = sum(t.monto for t in transacciones if isinstance(t, Ingreso))
    total_gastos = sum(t.monto for t in transacciones if isinstance(t, Gasto))
    for t in transacciones:
        print(f"  {t}")
    print(LINEA)
    print(f"  Total ingresos : +${total_ingresos:>12,.0f}")
    print(f"  Total gastos   : -${total_gastos:>12,.0f}")
    print(f"  Balance        :  ${total_ingresos - total_gastos:>12,.0f}")


def menu_metas(metas, gestor_archivos):
    while True:
        encabezado("Metas de Ahorro")
        print("  1. Nueva meta")
        print("  2. Agregar dinero a meta")
        print("  3. Ver metas")
        print("  0. Volver")
        op = input("  Opcion: ").strip()
        if op == "1":
            nombre = input("  Nombre de la meta: ")
            emoji = input("  Emoji (ej. airplane, car, house): ")
            categoria = input("  Categoria: ")
            objetivo = float(input("  Monto objetivo: $"))
            fecha = input("  Fecha limite (YYYY-MM-DD): ")
            meta = Meta(nombre, emoji, categoria, objetivo, fecha)
            metas.append(meta)
            gestor_archivos.guardar_metas(metas)
            print(f"  Meta '{nombre}' creada.")
        elif op == "2":
            if not metas:
                print("  Sin metas creadas.")
                continue
            for i, m in enumerate(metas):
                print(f"  {i+1}. {m}")
            idx = int(input("  Numero de meta: ")) - 1
            monto = float(input("  Monto a agregar: $"))
            metas[idx].agregar_dinero(monto)
            gestor_archivos.guardar_metas(metas)
            print(f"  Progreso actualizado: {metas[idx].calcular_progreso():.1f}%")
        elif op == "3":
            if not metas:
                print("  Sin metas.")
            for m in metas:
                print(f"  {m}")
        elif op == "0":
            break


def menu_tarjetas(tarjetas, gestor_archivos):
    while True:
        encabezado("Tarjetas de Credito")
        print("  1. Nueva tarjeta")
        print("  2. Registrar pago")
        print("  3. Ver tarjetas")
        print("  0. Volver")
        op = input("  Opcion: ").strip()
        if op == "1":
            nombre = input("  Nombre de la tarjeta: ")
            cupo = float(input("  Cupo total: $"))
            saldo = float(input("  Saldo actual (deuda): $"))
            dia_corte = int(input("  Dia de corte: "))
            dia_pago = int(input("  Dia de pago: "))
            tarjeta = TarjetaCredito(nombre, cupo, saldo, dia_corte=dia_corte, dia_pago=dia_pago)
            tarjetas.append(tarjeta)
            gestor_archivos.guardar_tarjetas(tarjetas)
            print(f"  Tarjeta '{nombre}' registrada.")
        elif op == "2":
            if not tarjetas:
                print("  Sin tarjetas registradas.")
                continue
            for i, t in enumerate(tarjetas):
                print(f"  {i+1}. {t}")
            idx = int(input("  Numero de tarjeta: ")) - 1
            monto = float(input("  Monto del pago: $"))
            tarjetas[idx].registrar_pago(monto)
            gestor_archivos.guardar_tarjetas(tarjetas)
            print("  Pago registrado.")
        elif op == "3":
            if not tarjetas:
                print("  Sin tarjetas.")
            for t in tarjetas:
                print(f"  {t}")
        elif op == "0":
            break


def resumen_presupuesto(transacciones, gestor_presupuesto):
    encabezado("Resumen por Categoria")
    categorias = gestor_presupuesto.categorias
    if not categorias:
        print("  Sin categorias configuradas.")
        return
    for cat in categorias:
        gasto = gestor_presupuesto.calcular_gasto_categoria(transacciones, cat)
        limite = gestor_presupuesto.obtener_limite(cat)
        if limite > 0:
            pct = (gasto / limite) * 100
            estado = "OK" if gasto <= limite else "EXCEDIDO"
            print(f"  {cat:<20} ${gasto:>10,.0f} / ${limite:>10,.0f}  ({pct:.0f}%)  {estado}")
        else:
            print(f"  {cat:<20} ${gasto:>10,.0f}  (sin limite)")


def login_o_registro(gestor_archivos) -> Usuario:
    encabezado("PersonalBudgetManager — Inicio de sesion")
    print("  1. Iniciar sesion")
    print("  2. Crear cuenta")
    op = input("  Opcion: ").strip()
    if op == "1":
        username = input("  Usuario: ")
        usuario = gestor_archivos.cargar_usuario(username)
        if not usuario:
            print("  Usuario no encontrado.")
            sys.exit(1)
        password = input("  Contrasena: ")
        if not usuario.autenticar(password):
            print("  Contrasena incorrecta.")
            sys.exit(1)
        print(f"  Bienvenido, {usuario.nombre}!")
        return usuario
    else:
        nombre = input("  Nombre completo: ")
        username = input("  Nombre de usuario: ")
        password = input("  Contrasena: ")
        usuario = Usuario(nombre, username, password)
        gestor_archivos.guardar_usuario(usuario)
        print(f"  Cuenta creada. Bienvenido, {nombre}!")
        return usuario


def main():
    gestor_archivos = GestorArchivos("data")
    gestor_presupuesto = GestorPresupuesto()
    gestor_presupuesto.agregar_limite("Alimentacion", 400000)
    gestor_presupuesto.agregar_limite("Transporte", 150000)
    gestor_presupuesto.agregar_limite("Entretenimiento", 200000)
    gestor_presupuesto.agregar_categoria("Trabajo")
    gestor_presupuesto.agregar_categoria("Extra")

    usuario = login_o_registro(gestor_archivos)
    transacciones = gestor_archivos.cargar_transacciones()
    metas = gestor_archivos.cargar_metas()
    tarjetas = gestor_archivos.cargar_tarjetas()

    while True:
        opcion = menu_principal()
        if opcion == "1":
            registrar_ingreso(transacciones, gestor_archivos, gestor_presupuesto)
        elif opcion == "2":
            registrar_gasto(transacciones, gestor_archivos, gestor_presupuesto)
        elif opcion == "3":
            ver_transacciones(transacciones)
        elif opcion == "4":
            menu_metas(metas, gestor_archivos)
        elif opcion == "5":
            menu_tarjetas(tarjetas, gestor_archivos)
        elif opcion == "6":
            resumen_presupuesto(transacciones, gestor_presupuesto)
        elif opcion == "0":
            print(f"\n  Hasta luego, {usuario.nombre}!\n")
            break
        else:
            print("  Opcion invalida.")


if __name__ == "__main__":
    main()

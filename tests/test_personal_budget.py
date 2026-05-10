import sys
import os
import unittest
import shutil

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modelos.ingreso import Ingreso
from modelos.gasto import Gasto
from modelos.usuario import Usuario
from modelos.meta import Meta
from modelos.tarjeta_credito import TarjetaCredito
from gestores.gestor_presupuesto import GestorPresupuesto
from gestores.gestor_archivos import GestorArchivos


class TestTransacciones(unittest.TestCase):

    def test_ingreso_atributos(self):
        ingreso = Ingreso(2500000, "Salario mensual", "Trabajo")
        self.assertEqual(ingreso.monto, 2500000)
        self.assertEqual(ingreso.categoria, "Trabajo")
        self.assertEqual(ingreso.descripcion, "Salario mensual")

    def test_gasto_atributos(self):
        gasto = Gasto(85000, "Supermercado", "Alimentacion")
        self.assertEqual(gasto.monto, 85000)
        self.assertEqual(gasto.categoria, "Alimentacion")

    def test_gasto_verifica_limite_dentro(self):
        gasto = Gasto(80000, "Mercado", "Alimentacion")
        self.assertTrue(gasto.verificar_limite(100000))

    def test_gasto_verifica_limite_excedido(self):
        gasto = Gasto(150000, "Ropa", "Vestuario")
        self.assertFalse(gasto.verificar_limite(100000))

    def test_gasto_verifica_limite_exacto(self):
        gasto = Gasto(100000, "Restaurante", "Alimentacion")
        self.assertTrue(gasto.verificar_limite(100000))

    def test_polimorfismo_registrar(self):
        transacciones = [
            Ingreso(500000, "Salario", "Trabajo"),
            Gasto(80000, "Mercado", "Alimentacion"),
        ]
        for t in transacciones:
            t.registrar()

    def test_polimorfismo_str(self):
        transacciones = [
            Ingreso(500000, "Salario", "Trabajo"),
            Gasto(80000, "Mercado", "Alimentacion"),
        ]
        for t in transacciones:
            resultado = str(t)
            self.assertIsInstance(resultado, str)
            self.assertGreater(len(resultado), 0)

    def test_ingreso_meta_id(self):
        ingreso = Ingreso(300000, "Freelance", "Extra", meta_id="abc123")
        self.assertEqual(ingreso.meta_id, "abc123")

    def test_transaccion_es_abstracta(self):
        from modelos.transaccion import Transaccion
        with self.assertRaises(TypeError):
            Transaccion(100, "test", "cat")


class TestUsuario(unittest.TestCase):

    def setUp(self):
        self.usuario = Usuario("Diunis", "diup", "1234")

    def test_autenticacion_correcta(self):
        self.assertTrue(self.usuario.autenticar("1234"))

    def test_autenticacion_incorrecta(self):
        self.assertFalse(self.usuario.autenticar("wrongpass"))

    def test_str_contiene_nombre(self):
        self.assertIn("Diunis", str(self.usuario))

    def test_str_contiene_username(self):
        self.assertIn("diup", str(self.usuario))

    def test_password_no_almacenada_en_texto_plano(self):
        self.assertNotEqual(self.usuario.password, "1234")

    def test_id_asignado(self):
        self.assertIsNotNone(self.usuario.id)
        self.assertGreater(len(self.usuario.id), 0)


class TestMeta(unittest.TestCase):

    def setUp(self):
        self.meta = Meta("Viaje a Paris", "airplane", "Viajes", 3000000, "2026-12-31")

    def test_progreso_inicial_cero(self):
        self.assertEqual(self.meta.calcular_progreso(), 0.0)

    def test_agregar_dinero_progreso(self):
        self.meta.agregar_dinero(1500000)
        self.assertAlmostEqual(self.meta.calcular_progreso(), 50.0)

    def test_meta_se_completa(self):
        self.meta.agregar_dinero(3000000)
        self.assertTrue(self.meta.completada)

    def test_meta_no_supera_100_porciento(self):
        self.meta.agregar_dinero(5000000)
        self.assertEqual(self.meta.calcular_progreso(), 100.0)

    def test_retirar_dinero(self):
        self.meta.agregar_dinero(1000000)
        self.meta.retirar_dinero(300000)
        self.assertEqual(self.meta.monto_actual, 700000)

    def test_retirar_no_va_negativo(self):
        self.meta.retirar_dinero(999999)
        self.assertEqual(self.meta.monto_actual, 0.0)

    def test_str_meta(self):
        resultado = str(self.meta)
        self.assertIn("Viaje a Paris", resultado)


class TestTarjetaCredito(unittest.TestCase):

    def setUp(self):
        self.tarjeta = TarjetaCredito("Visa Oro", 5000000, saldo_actual=1200000,
                                      dia_corte=25, dia_pago=10)

    def test_calcular_disponible(self):
        self.assertEqual(self.tarjeta.calcular_disponible(), 3800000)

    def test_calcular_uso_porcentaje(self):
        self.assertAlmostEqual(self.tarjeta.calcular_uso(), 24.0)

    def test_registrar_pago_reduce_saldo(self):
        self.tarjeta.registrar_pago(200000)
        self.assertEqual(self.tarjeta.saldo_actual, 1000000)

    def test_pago_no_va_negativo(self):
        self.tarjeta.registrar_pago(9999999)
        self.assertEqual(self.tarjeta.saldo_actual, 0.0)

    def test_str_tarjeta(self):
        resultado = str(self.tarjeta)
        self.assertIn("Visa Oro", resultado)


class TestGestorPresupuesto(unittest.TestCase):

    def setUp(self):
        self.gestor = GestorPresupuesto()
        self.gestor.agregar_limite("Alimentacion", 400000)
        self.gestor.agregar_limite("Transporte", 150000)

    def test_obtener_limite_existente(self):
        self.assertEqual(self.gestor.obtener_limite("Alimentacion"), 400000)

    def test_obtener_limite_inexistente_retorna_cero(self):
        self.assertEqual(self.gestor.obtener_limite("Viajes"), 0.0)

    def test_agregar_categoria(self):
        self.gestor.agregar_categoria("Entretenimiento")
        self.assertIn("Entretenimiento", self.gestor.categorias)

    def test_no_duplica_categoria(self):
        self.gestor.agregar_categoria("Alimentacion")
        conteo = self.gestor.categorias.count("Alimentacion")
        self.assertEqual(conteo, 1)

    def test_calcular_gasto_categoria(self):
        txns = [
            Gasto(80000, "Mercado", "Alimentacion"),
            Gasto(50000, "Restaurante", "Alimentacion"),
            Ingreso(500000, "Salario", "Trabajo"),
            Gasto(30000, "Bus", "Transporte"),
        ]
        total = self.gestor.calcular_gasto_categoria(txns, "Alimentacion")
        self.assertEqual(total, 130000)

    def test_calcular_gasto_categoria_vacia(self):
        total = self.gestor.calcular_gasto_categoria([], "Alimentacion")
        self.assertEqual(total, 0.0)


class TestGestorArchivos(unittest.TestCase):

    def setUp(self):
        self.gestor = GestorArchivos("data_test_tmp")

    def tearDown(self):
        if os.path.exists("data_test_tmp"):
            shutil.rmtree("data_test_tmp")

    def test_guardar_y_cargar_usuario(self):
        usuario = Usuario("Diunis", "diup_test", "pass123")
        self.gestor.guardar_usuario(usuario)
        cargado = self.gestor.cargar_usuario("diup_test")
        self.assertIsNotNone(cargado)
        self.assertEqual(cargado.nombre, "Diunis")
        self.assertTrue(cargado.autenticar("pass123"))

    def test_cargar_usuario_inexistente(self):
        resultado = self.gestor.cargar_usuario("nadie")
        self.assertIsNone(resultado)

    def test_guardar_y_cargar_transacciones(self):
        txns = [
            Ingreso(500000, "Salario", "Trabajo"),
            Gasto(80000, "Mercado", "Alimentacion"),
        ]
        self.gestor.guardar_transacciones(txns)
        cargadas = self.gestor.cargar_transacciones()
        self.assertEqual(len(cargadas), 2)
        self.assertIsInstance(cargadas[0], Ingreso)
        self.assertIsInstance(cargadas[1], Gasto)

    def test_guardar_y_cargar_metas(self):
        metas = [Meta("Viaje", "airplane", "Viajes", 3000000, "2026-12-31")]
        self.gestor.guardar_metas(metas)
        cargadas = self.gestor.cargar_metas()
        self.assertEqual(len(cargadas), 1)
        self.assertEqual(cargadas[0].nombre, "Viaje")

    def test_guardar_y_cargar_tarjetas(self):
        tarjetas = [TarjetaCredito("Mastercard", 8000000, 2000000)]
        self.gestor.guardar_tarjetas(tarjetas)
        cargadas = self.gestor.cargar_tarjetas()
        self.assertEqual(len(cargadas), 1)
        self.assertEqual(cargadas[0].nombre, "Mastercard")
        self.assertEqual(cargadas[0].saldo_actual, 2000000)

    def test_cargar_transacciones_sin_archivo(self):
        resultado = self.gestor.cargar_transacciones()
        self.assertEqual(resultado, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)

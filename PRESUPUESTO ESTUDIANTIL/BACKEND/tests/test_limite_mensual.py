"""
Pruebas Unitarias para la Regla: ¿El límite mensual es válido?
IHC Clase 14 - Del requisito al código
Proyecto: Presupuesto Estudiantil
"""

import pytest
from reglas_presupuesto import es_limite_mensual_valido


def test_01_caso_permitido_limite_valido():
    """
    Caso permitido:
    El estudiante tiene 70 Bs gastados y 700 Bs de saldo total.
    Ingresa un límite mensual de 500 Bs -> Es válido (True).
    """
    assert es_limite_mensual_valido(limite=500.0, gastos_mes=70.0, saldo_maximo=700.0) is True


def test_02_caso_rechazado_limite_cero_o_negativo():
    """
    Caso rechazado:
    Un límite de 0 Bs o un número negativo (-100 Bs) no es válido (False).
    """
    assert es_limite_mensual_valido(limite=0.0, gastos_mes=70.0, saldo_maximo=700.0) is False
    assert es_limite_mensual_valido(limite=-50.0, gastos_mes=70.0, saldo_maximo=700.0) is False


def test_03_caso_rechazado_limite_menor_a_gastos_actuales():
    """
    Caso rechazado:
    Si ya gastó 70 Bs en el mes, no puede poner un límite de 50 Bs (False).
    """
    assert es_limite_mensual_valido(limite=50.0, gastos_mes=70.0, saldo_maximo=700.0) is False


def test_04_caso_rechazado_limite_supera_saldo_maximo():
    """
    Caso rechazado:
    Si el saldo base es 700 Bs, un límite de 1200 Bs no es realista y se rechaza (False).
    """
    assert es_limite_mensual_valido(limite=1200.0, gastos_mes=70.0, saldo_maximo=700.0) is False


def test_05_caso_rechazado_valores_nulos_o_invalidos():
    """
    Caso rechazado:
    Valores None o textos no numéricos deben rechazarse (False).
    """
    assert es_limite_mensual_valido(limite=None) is False
    assert es_limite_mensual_valido(limite="quinientos") is False


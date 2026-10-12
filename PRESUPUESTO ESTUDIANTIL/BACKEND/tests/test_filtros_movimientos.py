"""
Pruebas de la búsqueda y los filtros de movimientos
Issue #2: Buscar y filtrar movimientos

Parte 1: reglas puras (validar filtros, periodos y totales).
Parte 2: filtrado en la consulta a la base de datos.
Parte 3: flujo completo por la API.
"""

from datetime import date
import pytest
import models
from filtros_movimientos import (
    crear_filtros, rango_del_periodo, consultar_movimientos, calcular_totales, Filtros
)

HOY = date(2026, 10, 15)


# ===================== Parte 1: reglas puras =====================

def test_01_este_mes_va_del_primer_al_ultimo_dia():
    assert rango_del_periodo(Filtros(periodo="este_mes"), HOY) == (date(2026, 10, 1), date(2026, 10, 31))


def test_02_mes_anterior_cruza_el_cambio_de_anio():
    assert rango_del_periodo(Filtros(periodo="mes_anterior"), date(2026, 1, 10)) == (date(2025, 12, 1), date(2025, 12, 31))


def test_03_rango_de_fechas_valido():
    filtros = crear_filtros(periodo="rango", desde="2026-10-01", hasta="2026-10-10")
    assert rango_del_periodo(filtros, HOY) == (date(2026, 10, 1), date(2026, 10, 10))


@pytest.mark.parametrize("argumentos", [
    {"tipo": "prestamo"},
    {"estado": "cancelado"},
    {"periodo": "semana"},
    {"periodo": "rango", "desde": "2026-10-01"},
    {"periodo": "rango", "desde": "2026-10-20", "hasta": "2026-10-01"},
    {"periodo": "rango", "desde": "ayer", "hasta": "2026-10-01"},
])
def test_04_filtros_invalidos_se_rechazan_con_motivo(argumentos):
    with pytest.raises(ValueError):
        crear_filtros(**argumentos)


def test_05_totales_separan_ingresos_y_gastos():
    lista = [
        {"tipo": "gasto", "monto": 25.5},
        {"tipo": "gasto", "monto": 10},
        {"tipo": "ingreso", "monto": 300},
    ]
    assert calcular_totales(lista) == {"cantidad": 3, "total_ingresos": 300.0, "total_gastos": 35.5}


def test_06_totales_sin_resultados_son_cero():
    assert calcular_totales([]) == {"cantidad": 0, "total_ingresos": 0.0, "total_gastos": 0.0}


# ============ Parte 2: filtrado en la base de datos ============

@pytest.fixture
def datos(db_session):
    """Movimientos de ejemplo del usuario 1 y un movimiento de otro usuario."""
    comida = models.Categoria(nombre="Comida y Almuerzos", tipo="gasto")
    transporte = models.Categoria(nombre="Transporte y Pasajes", tipo="gasto")
    beca = models.Categoria(nombre="Beca Universitaria", tipo="ingreso")
    otro = models.Usuario(id=2, nombre="Otro", email="otro@universidad.edu", password_hash="x")
    db_session.add_all([comida, transporte, beca, otro])
    db_session.flush()

    def mov(desc, monto, tipo, cat, fecha, estado="pendiente", usuario_id=1):
        return models.Movimiento(usuario_id=usuario_id, descripcion=desc, monto=monto, tipo=tipo,
                                 categoria_id=cat.id if cat else None, fecha=fecha, estado=estado)

    db_session.add_all([
        mov("Almuerzo menú", 15, "gasto", comida, date(2026, 10, 3), "pagado"),
        mov("Cena con amigos", 40, "gasto", comida, date(2026, 10, 12)),
        mov("Pasaje micro", 2.5, "gasto", transporte, date(2026, 10, 5), "pagado"),
        mov("Almuerzo facultad", 12, "gasto", comida, date(2026, 9, 20), "pagado"),
        mov("Beca octubre", 500, "ingreso", beca, date(2026, 10, 1)),
        mov("Fotocopias", 8, "gasto", None, date(2026, 10, 7)),
        mov("Almuerzo de otro usuario", 99, "gasto", comida, date(2026, 10, 3), usuario_id=2),
    ])
    db_session.commit()
    return db_session


def descripciones(db, **filtros):
    return [m.descripcion for m in consultar_movimientos(db, 1, crear_filtros(**filtros), HOY)]


def test_07_buscar_por_descripcion_sin_importar_mayusculas(datos):
    assert descripciones(datos, texto="PASAJE") == ["Pasaje micro"]
    assert sorted(descripciones(datos, texto="cena")) == ["Cena con amigos"]


def test_08_buscar_por_concepto_categoria(datos):
    """'almuerzo' encuentra también 'Cena con amigos' porque su categoría es 'Comida y Almuerzos'."""
    assert descripciones(datos, texto="transporte") == ["Pasaje micro"]
    assert sorted(descripciones(datos, texto="almuerzo")) == ["Almuerzo facultad", "Almuerzo menú", "Cena con amigos"]


def test_09_filtrar_por_tipo(datos):
    assert descripciones(datos, tipo="ingreso") == ["Beca octubre"]


def test_10_filtrar_por_categoria_y_sin_categoria(datos):
    assert len(descripciones(datos, categoria="Comida y Almuerzos")) == 3
    assert descripciones(datos, categoria="General") == ["Fotocopias"]


def test_11_filtrar_por_estado(datos):
    assert sorted(descripciones(datos, estado="pagado")) == ["Almuerzo facultad", "Almuerzo menú", "Pasaje micro"]


def test_12_filtrar_por_periodo(datos):
    assert descripciones(datos, periodo="mes_anterior") == ["Almuerzo facultad"]
    assert len(descripciones(datos, periodo="este_mes")) == 5
    assert descripciones(datos, periodo="rango", desde="2026-10-04", hasta="2026-10-06") == ["Pasaje micro"]


def test_13_caso_con_resultados_filtros_combinados(datos):
    """Gastos de comida de este mes: combina tipo, categoría y periodo."""
    resultado = consultar_movimientos(
        datos, 1, crear_filtros(tipo="gasto", categoria="Comida y Almuerzos", periodo="este_mes"), HOY)
    assert sorted(m.descripcion for m in resultado) == ["Almuerzo menú", "Cena con amigos"]
    assert calcular_totales([{"tipo": m.tipo, "monto": m.monto} for m in resultado])["total_gastos"] == 55.0


def test_14_caso_sin_resultados(datos):
    resultado = consultar_movimientos(datos, 1, crear_filtros(texto="almuerzo", periodo="mes_anterior", estado="pendiente"), HOY)
    assert resultado == []


def test_15_nunca_muestra_movimientos_de_otro_usuario(datos):
    assert "Almuerzo de otro usuario" not in descripciones(datos, texto="almuerzo")


def test_16_comodines_se_buscan_como_texto(datos):
    """Un '%' escrito por el estudiante no debe traer todos los movimientos."""
    assert descripciones(datos, texto="%") == []


# ===================== Parte 3: flujo por la API =====================

def test_17_api_total_coincide_con_la_lista(client, datos):
    res = client.get("/movimientos/filtrar", params={"q": "almuerzo"})
    assert res.status_code == 200
    cuerpo = res.json()
    assert cuerpo["cantidad"] == len(cuerpo["movimientos"]) == 3
    assert cuerpo["total_gastos"] == sum(m["monto"] for m in cuerpo["movimientos"]) == 67.0


def test_18_api_sin_resultados_devuelve_lista_vacia_y_total_cero(client, datos):
    cuerpo = client.get("/movimientos/filtrar", params={"q": "zapatos"}).json()
    assert cuerpo == {"movimientos": [], "cantidad": 0, "total_ingresos": 0.0, "total_gastos": 0.0}


def test_19_api_filtro_invalido_explica_el_motivo(client):
    res = client.get("/movimientos/filtrar", params={"periodo": "rango", "desde": "2026-10-20", "hasta": "2026-10-01"})
    assert res.status_code == 400
    assert "posterior" in res.json()["detail"]


def test_20_gastos_de_este_mes_coinciden_con_el_gastado_del_limite(client):
    """Relación con el issue #1: el total filtrado de este mes = 'gastado del mes' del límite."""
    hoy = date.today().isoformat()
    # Dinero recibido para poder registrar un gasto ya pagado (la app empieza en 0 Bs)
    client.post("/movimientos", json={"descripcion": "Mesada", "monto": 100, "tipo": "ingreso",
                                      "fecha": hoy, "estado": "pagado"})
    for monto, estado in [(30, "pagado"), (12.5, "pendiente")]:
        client.post("/movimientos", json={"descripcion": "Gasto", "monto": monto, "tipo": "gasto",
                                          "fecha": hoy, "estado": estado})
    client.post("/movimientos", json={"descripcion": "Beca", "monto": 400, "tipo": "ingreso", "fecha": hoy})

    filtrado = client.get("/movimientos/filtrar", params={"tipo": "gasto", "periodo": "este_mes"}).json()
    assert filtrado["total_gastos"] == client.get("/limite").json()["gastado_mes"] == 42.5

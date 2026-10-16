# Actividad Clase 16: Decisiones de Interacción
## Del hallazgo a la decisión (Fitts, Hick y Carga Cognitiva)

**Materia:** Interacción Humano-Computador (IHC) — Proyecto 2  
**Estudiante:** Carmen Jenifer Aranibar Fernandez  
**Aplicación:** Presupuesto Estudiantil  
**Tema Asignado (Lámina 17):** *Presupuesto: Registrar gasto · categorías · límite y disponible*  
**Objetivo:** Documentar un hallazgo por principio (Fitts, Hick y Carga Cognitiva), priorizar uno por su impacto en la tarea, implementar su corrección en el código y verificarlo en funcionamiento.

> *"No buscamos decorar. Buscamos reducir esfuerzo físico y mental durante una tarea concreta. Las heurísticas señalan el problema; hoy afinaremos la solución."*

---

## 1. Registro de los Tres Hallazgos (Láminas 16 y 18)

| # | Principio | Captura Obligatoria | Elemento y Problema Observado | Justificación Breve de Interacción | Estado al Terminar |
|---|---|---|---|---|:---:|
| **1** | **Ley de Fitts**<br>*(Esfuerzo motor / Alcanzar)* | `docs/evidencias/clase-16/fitts-hallazgo.png`<br>![Hallazgo Fitts](evidencias/clase-16/fitts-hallazgo.png) | **Botón de cierre modal "✕" pequeño y distante:**<br>En el modal de *Registrar Gasto*, el único control rápido para descartar la acción es un icono "✕" de apenas 24 px ubicado en la esquina superior derecha, a gran distancia del flujo visual y de los campos donde el estudiante interactúa. | **Tamaño y distancia:** El objetivo pequeño y alejado exige alta precisión motora y mayor tiempo de movimiento. No toda el área visible facilita el cierre seguro. | **Documentado.** |
| **2** | **Ley de Hick**<br>*(Esfuerzo de selección / Elegir)* | `docs/evidencias/clase-16/hick-hallazgo.png`<br>![Hallazgo Hick](evidencias/clase-16/hick-hallazgo.png) | **Selector plano de categorías sin jerarquía ni prioridad:**<br>Al desplegar el campo *Categoría*, se presentan 8 opciones simultáneas compitiendo al mismo nivel (`Comida y Almuerzos`, `Transporte y Pasajes`, `Fotocopias y Material`, `Internet y Saldo`, `Vivienda y Alquiler`, `Salud y Medicamentos`, `Ocio y Salidas`, `Otros Gastos`), sin destacar las más habituales de un universitario. | **Cantidad y prioridad:** Demasiadas alternativas compiten al mismo tiempo. No existe agrupación temática ni prioridad para los gastos cotidianos más frecuentes, aumentando el tiempo de decisión. | **Documentado.** |
| **3** | **Carga Cognitiva**<br>*(Esfuerzo mental / Comprender)* | `docs/evidencias/clase-16/carga-cognitiva-hallazgo.png`<br>![Hallazgo Carga Cognitiva](evidencias/clase-16/carga-cognitiva-hallazgo.png) | **Ausencia de proyección del disponible al definir o modificar el límite:**<br>En el modal *Límite mensual*, el estudiante ingresa una cifra (ej. `600 Bs`), pero el sistema únicamente le recuerda *"Ya llevas gastado X Bs"*. No muestra en tiempo real cuánto dinero le quedará disponible si aplica ese límite. Obliga al estudiante a realizar mentalmente una resta aritmética manual (`Nuevo Límite − Gastado = Disponible`). | **Memoria y cálculo innecesario:** La interfaz no proyecta el resultado de la decisión en el contexto en que se usa; obliga a gastar memoria de trabajo en una resta mental que el sistema debe calcular de inmediato. | **Documentado.** |

---

## 2. Priorización del Hallazgo (Lámina 16)

> **Consigna:** *No necesitan corregir los tres hoy. Deben documentar los tres, priorizar uno, terminar su corrección y comprobarla en la aplicación.*

### Hallazgo Seleccionado
👉 **Hallazgo #3: Carga Cognitiva — Proyección en tiempo real del saldo disponible resultante al definir o modificar el límite mensual.**

### Justificación de la Elección
1. **Alineación directa con el tema asignado:**  
   La funcionalidad asignada para nuestro grupo es explícitamente: ***«Registrar gasto · categorías · límite y disponible»***. El valor de fijar un presupuesto o límite radica en conocer con certeza cuánto dinero *disponible* le queda al estudiante para sobrevivir el mes. Si el modal obliga a calcular ese número con la mente, el sistema falla en su propósito principal.
2. **Eliminación de trabajo mental innecesario (Láminas 11 y 13):**  
   Tal como establece la diapositiva de Carga Cognitiva: *"La interfaz no debe gastar memoria en trabajo innecesario"*. Forzar al usuario a recordar cuánto lleva gastado y restarlo manualmente del número que tipea sobrecarga la memoria de trabajo. El sistema debe mostrar el dato visible y contextualizado en tiempo real.
3. **Impacto real en la toma de decisiones financieras:**  
   Al ver instantáneamente el impacto del nuevo límite (*«✓ Con este límite tendrás X.XX Bs disponibles este mes»* o *«⚠️ Este límite no te deja saldo disponible»*), el estudiante ajusta su presupuesto de forma informada sin ensayo y error.

---

## 3. Corrección Implementada (Commit 2)

### 3.1 Solución en Código Frontend (`MovimientosView.vue`)
Se implementó una propiedad computada reactiva y un bloque visual de retroalimentación en el modal de límite:

1. **Lógica computada reactiva (`nuevoDisponibleEstimado`):**
   Evalúa en tiempo real el valor ingresado en `limiteEscrito` comparándolo contra `limiteInfo.gastado_mes`:
   - Si el límite escrito es mayor a lo gastado: calcula la diferencia exacta (`nuevo_limite - gastado_mes`).
   - Si el límite escrito es menor o igual a lo gastado: identifica el estado de alerta preventiva sin saldo disponible.

2. **Caja visual de proyección contextual en el modal:**
   Justo debajo del campo de entrada de dinero, se despliega una tarjeta de confirmación en tiempo real:
   - **Verde / Informativo:** `✓ Con este límite tendrás X.XX Bs disponibles este mes.`
   - **Ámbar / Alerta:** `⚠️ Atención: Con este límite no tendrás disponible (ya llevas gastado X.XX Bs).`

### 3.2 Evidencia del Después (Corrección Obligatoria)
- **Captura:** `docs/evidencias/clase-16/carga-cognitiva-despues.png`  
  ![Corrección Carga Cognitiva](evidencias/clase-16/carga-cognitiva-despues.png)
- **Resultado:** El usuario tipea el monto deseado y ve inmediatamente cuánto saldo disponible tendrá sin hacer ningún cálculo mental.

---

## 4. Trazabilidad de Commits (Lámina 18)

1. **Commit 1:**  
   `docs: registrar hallazgos de interacción`  
   *Registra la documentación completa de los tres hallazgos (Fitts, Hick y Carga Cognitiva) y la priorización.*

2. **Commit 2:**  
   `fix: aplicar mejora de interacción`  
   *Aplica la lógica reactiva en `MovimientosView.vue` y añade la captura del después en `docs/evidencias/clase-16/carga-cognitiva-despues.png`.*

# Actividad Clase 15: Heurísticas de Nielsen - Presupuesto Estudiantil

**Materia:** Interacción Humano-Computador (IHC) - Proyecto 2  
**Estudiante:** Carmen Jenifer Aranibar Fernandez  
**Aplicación:** Presupuesto Estudiantil  
**Acción asignada (Imagen 3):** Configurar el límite y registrar un gasto  
**Objetivo de la actividad (Imagen 1):** Encontrar tres hallazgos y comenzar una mejora en 35 minutos.  
 **Consigna:** *Registren tres problemas observables y relaciónenlos con heurísticas. (Imagen 2: Registren los tres hallazgos antes de elegir uno).*

### Tabla de Evidencia y Registro de Hallazgos

| # | Pantalla y evidencia | Problema y consecuencia | Heurística | Severidad |
|---|----------------------|-------------------------|------------|:---------:|
| **1** | **Modal "Registrar Movimiento"**<br>*(Formulario modal que se abre al pulsar `+ Registrar Movimiento`)* | **Falta de visibilidad del límite disponible al momento de registrar el gasto:**<br>El modal cubre la pantalla con un fondo oscuro (overlay) y oculta el panel de límite. Dentro del formulario no se indica cuánto saldo disponible queda este mes.<br>**Consecuencia:** El estudiante debe memorizar su saldo disponible antes de abrir el modal. Si no lo recuerda o calcula mal, ingresa un monto excesivo y es bloqueado recién al intentar guardar, generando frustración, incertidumbre y retrabajo. | **H6: Reconocimiento antes que recuerdo**<br>*(y H1: Visibilidad del estado del sistema)*<br>El usuario no debería tener que recordar información de una pantalla previa; los datos indispensables para tomar la decisión deben estar visibles en el contexto de la acción. | **3**<br>*(Mayor)* |
| **2** | **Campo "Cantidad" en Modal de Registro**<br>*(Input numérico `input-cantidad` del formulario de gasto)* | **Ausencia de retroalimentación preventiva en tiempo real al escribir:**<br>El campo permite tipear cualquier cantidad sin alertar preventivamente mientras se escribe que el monto sobrepasa el límite mensual disponible.<br>**Consecuencia:** El estudiante invierte tiempo completando todos los demás campos (descripción, categoría, día, mes) solo para descubrir al final que el formulario será rechazado al hacer clic en "Guardar". | **H5: Prevención de errores**<br>Es mucho mejor prevenir que ocurra el error mediante micro-retroalimentación reactiva antes que esperar a que el usuario complete y envíe el formulario para mostrarle un mensaje de error. | **2**<br>*(Menor / Medio)* |
| **3** | **Modal "Límite mensual"**<br>*(Diálogo modal al hacer clic en `Definir límite` o `Cambiar límite`)* | **Imposibilidad de eliminar o restablecer el límite una vez configurado:**<br>Una vez que el estudiante define un límite mensual (ej. 500 Bs), la interfaz no ofrece ninguna opción o botón para "Quitar límite" o volver al estado inicial sin restricción. Si el usuario borra el campo e intenta guardar en blanco, el sistema lanza un error exigiendo un número mayor a 0.<br>**Consecuencia:** El usuario queda cautivo en un régimen restrictivo forzoso si cambian sus condiciones económicas en el mes. | **H3: Control y libertad del usuario**<br>El sistema debe proveer una "salida de emergencia" claramente visible para revertir configuraciones o salir de un estado no deseado sin obstáculos. | **3**<br>*(Mayor)* |

---

## 3. Priorizar (15–20 min)

> **Consigna:** *Asignen severidad y elijan un hallazgo. (Imagen 2: Elijan el hallazgo por su impacto en la tarea, no porque sea el cambio visual más rápido).*

### Hallazgo Seleccionado
👉 **Hallazgo #1: Falta de visibilidad del límite disponible dentro del formulario de registro de gasto (Heurísticas H6 y H1, Severidad 3).**

### Justificación de la Elección
1. **Impacto directo en la tarea asignada:**  
   La tarea asignada por la cátedra es explícitamente *"Configurar el límite y registrar un gasto"*. El valor de configurar un límite radica precisamente en orientar el comportamiento del usuario durante el registro del gasto. Si al momento crucial de registrar el gasto el sistema le oculta al estudiante cuánto dinero tiene disponible, la funcionalidad de límite queda desconectada de la acción práctica del usuario.
2. **Carga cognitiva innecesaria (H6 - Reconocimiento antes que recuerdo):**  
   Obliga al estudiante a memorizar números (`limiteInfo.disponible`) antes de pulsar el botón o a cancelar el modal para ir a mirar el dashboard y volver a abrirlo. En interfaces financieras, los datos de saldo/cupo deben acompañar siempre al campo donde se solicita ingresar dinero.
3. **No es simplemente un cambio cosmético rápido:**  
   A diferencia de cambiar un color o un texto estático, este hallazgo requiere **vincular el estado reactivo del presupuesto con el formulario modal**, calculando en tiempo real el dinero disponible del mes y cómo se verá impactado por el monto que se está ingresando.

---

## 4. Mejorar (20–32 min)

> **Consigna:** *Inicien un cambio pequeño en la interfaz y el código.*

### 4.1 Solución diseñada e implementada

Se intervino el archivo del frontend [`MovimientosView.vue`](file:///c:/Users/HP/Videos/PROYECTO2-IHC/PRESUPUESTO%20ESTUDIANTIL/FRONTEND/src/views/MovimientosView.vue):

1. **Indicador contextual de presupuesto:**  
   Dentro del modal *"Registrar Gasto"* (`abrirModal && !esDemo`), justo antes de los campos del formulario, se incorporó una tarjeta de contexto financiero que muestra:
   - El **saldo disponible del mes actual** con una insignia destacada (`badge-disp-ok` / `badge-disp-alerta`).
   - El límite total configurado y el monto que ya se lleva gastado.
2. **Cálculo preventivo en tiempo real (H5 y H6):**  
   Se creó una propiedad computada `excesoPreventivoGasto` que compara en vivo lo que el estudiante va escribiendo en el campo *"Cantidad"* contra el disponible del mes:
   - **Si el monto ingresado cabe en el presupuesto:** Muestra en verde un mensaje amigable indicando:  
     *«✓ Con este gasto te quedarán X.XX Bs disponibles.»*
   - **Si el monto excede el presupuesto:** Alerta inmediatamente en tono de advertencia antes de enviar el formulario:  
     *«⚠️ Atención: Esta cantidad supera tu límite disponible por X.XX Bs.»*
   - Si no hay límite mensual definido, el banner no interfiere.

---
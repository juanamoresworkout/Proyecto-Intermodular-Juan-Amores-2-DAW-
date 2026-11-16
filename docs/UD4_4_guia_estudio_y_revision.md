# UD4.4: guía de estudio y revisión final

Fecha de revisión: 16/11/2026.

Actualización posterior autorizada: se ha retirado el token CSRF explícito de
`base_create_update.html`. Las 18 pantallas generan ahora exactamente un token
mediante Crispy. Un POST vacío con token alcanza la validación (HTTP 200, sin
guardar); sin token es rechazado (403). El hallazgo de duplicación documentado
más abajo queda como antecedente resuelto. También se corrigieron la paginación
y el horario sin día: 36 enlaces recorridos en nueve listados conservaron el
orden válido en ambos sentidos; los POST de crear y actualizar un horario sin
día devolvieron el error de campo obligatorio, sin excepción ni cambios guardados.
Se rechazó un día inexistente y se aceptó el lunes con código 0. Los pendientes
de mensajes, comentarios y trazabilidad académica siguen abiertos.

Este documento explica la Actividad 4 implementada en el proyecto y contrasta el estado de la UD4 con las actividades, la teoría y la autoevaluación del profesor. Es una guía de estudio y evidencia de revisión, no una calificación definitiva. La aplicación tiene funcionalidad implementada, pero **no está todavía perfecta ni cerrada para entregar**: los pendientes se enumeran al final.

## 1. Documentos que mandan

- [Actividades del profesor](../.tmp/UD4%20-%20Actividades%20SERVIDOR%20(1).odt): requisitos y anexo de distribución de campos.
- [Autoevaluación del profesor](../.tmp/UD4%20-%20Actividades%20SERVIDOR%20-%20Autoevaluación.odt): códigos y puntuaciones.
- [Teoría del profesor](../.tmp/UD4%20-%20Multicapa%20–%20Vistas%20y%20controladores,%20eventos%20e%20interactividad-%20SERVIDOR.pdf): explicación de los mecanismos utilizados.

Se han leído las extracciones de los documentos, cotejado el contenido XML de los ODT originales y revisado visualmente las páginas 30, 31 y 32 del PDF. Para mensajes se contrastaron los apartados 3.5.1 y 3.5.2, páginas 12–16; para formularios y validación, el apartado 4; para Crispy, el apartado 6.1, páginas 29–33.

La Actividad 4 tiene **cinco** apartados, no cuatro como se afirmó anteriormente:

| Código | Qué pide | Puntuación |
|---|---|---:|
| UD4.4.a | Mensajes configurados; errores con clase Bootstrap correcta; éxito con representación del objeto en cada creación y actualización | 1 |
| UD4.4.b | Plantilla común renderizada con Crispy como en el ejemplo | 1 |
| UD4.4.c | Constructor `__init__`, helper y layout en cada formulario | 1 |
| UD4.4.d | Layouts de billing según el anexo I, tabla 2 | 3 |
| UD4.4.e | Al menos cinco layouts de core y completar su tabla del anexo | 4 |

## 2. Qué responsabilidad tiene cada pieza

| Pieza | Responsabilidad en este proyecto |
|---|---|
| Modelo | Define campos, relaciones y reglas persistentes |
| ModelForm | Construye campos, transforma los valores recibidos y valida datos |
| `clean_campo()` | Valida un campo concreto y devuelve su valor válido |
| `clean()` | Comprueba relaciones entre campos del formulario |
| Mixin | Comparte comportamiento entre vistas mediante herencia |
| CreateView / UpdateView | Procesa GET/POST, utiliza el formulario y guarda cuando corresponde |
| FormHelper | Configura cómo Crispy representa el formulario |
| Layout / Row / Column | Distribuye visualmente los campos |
| Etiqueta `{% crispy form %}` | Renderiza el formulario y su helper en HTML |
| Bootstrap 5 | Aplica estilos y distribución a las clases del HTML |
| Framework de mensajes | Transporta avisos entre la operación y la página de destino |

Crispy no decide si un cobro supera una factura ni guarda registros. Un mixin tampoco tiene que validar siempre: `DeleteContextMixin` prepara textos y `OrderingMixin` modifica el orden de una consulta.

## 3. Archivos que hemos preparado

| Archivo | Contenido relevante |
|---|---|
| [requirements.txt](../requirements.txt) | Versiones reproducibles de las dependencias |
| [reservas/settings.py](../reservas/settings.py) | Apps de mensajes/Crispy, Bootstrap 5 y etiqueta roja |
| [common/mixins.py](../common/mixins.py) | Contexto compartido, mensajes y redirecciones, protección de borrado y ordenación |
| [billing/forms.py](../billing/forms.py) | Tres ModelForm, validaciones positivas y layouts del anexo |
| [core/forms.py](../core/forms.py) | Seis ModelForm, tres validaciones y layouts propios |
| [billing/views.py](../billing/views.py), [core/views.py](../core/views.py) | `form_class`, herencia de mixins, textos y destinos |
| [base_create_update.html](../templates/common/base_create_update.html) | Plantilla común que usa Crispy y conserva los botones |
| [messages.html](../templates/common/messages.html) | Recorre los mensajes y construye la clase de alerta |

No se ha implementado la propuesta conceptual de relacionar factura y reserva ni el cliente genérico. Es una propuesta pendiente de aprobación académica, no parte del código revisado.

## 4. Instalación y configuración

En el entorno virtual `piapp-env` se instalaron:

```text
django-crispy-forms==2.7
crispy-bootstrap5==2026.9
```

La primera biblioteca interpreta los helpers y layouts. La segunda aporta las plantillas de Bootstrap 5. Las dos versiones quedaron registradas en `requirements.txt` sin cambiar las demás dependencias.

En `INSTALLED_APPS` se añadieron:

```python
'crispy_forms',
'crispy_bootstrap5',
```

Y se configuró:

```python
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'
```

La primera variable permite ese paquete; la segunda lo selecciona. Esto no descarga por sí mismo el CSS de Bootstrap para el navegador: la plantilla base ya enlaza Bootstrap 5.2.0.

## 5. Mensajes de éxito y error: UD4.4.a

El proyecto ya tenía `django.contrib.messages`, su middleware, el procesador de contexto y la inclusión de `messages.html` en la plantilla intranet.

```python
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}
```

Django llama `error` al nivel de error; Bootstrap utiliza `alert-danger`. Este mapeo permite que `alert-{{ message.tags }}` produzca el estilo rojo. Los mensajes de éxito usan `success` y producen `alert-success`.

### Mixin común de éxito

```python
class CreateUpdateSuccessMixin(SuccessMessageMixin):
    success_url_name = None
    success_message = None

    def get_success_url(self):
        return reverse_lazy(
            self.success_url_name,
            kwargs={'pk': self.object.pk},
        )

    def get_success_message(self, cleaned_data):
        return self.success_message.format(object=self.object)
```

- `SuccessMessageMixin` es la clase de Django que añade el aviso de éxito después del guardado correcto.
- Los atributos iniciales son valores que cada vista concreta sustituye.
- `self.object` es el objeto guardado; `pk` identifica ese objeto.
- `reverse_lazy` resuelve el nombre de una URL con los argumentos necesarios; no ejecuta la vista de destino.
- `get_success_message` sustituye `{object}` usando la representación del objeto, definida por su `__str__`.
- `cleaned_data` forma parte de la firma del método de Django; nuestro texto utiliza `self.object` y no necesita consultar ese argumento.

Por ejemplo, las vistas de cliente configuran `success_url_name = 'cliente_update'`. La creación usa `Cliente '{object}' creado correctamente.` y la actualización cambia el verbo a `actualizado`.

En cobros y reservas, el mixin de negocio aparece antes del de éxito:

```python
class CobroCreateView(
    CobroMixin,
    CreateUpdateSuccessMixin,
    CreateUpdateContextMixin,
    CreateView,
):
    # El resto de atributos está definido en billing/views.py.
    pass
```

Python sigue el orden de resolución de métodos (MRO). En esta herencia, el `form_valid` de cobros comprueba la suma antes de continuar con `super()`. Si rechaza el formulario, no llega al guardado ni al aviso de éxito. `CobroMixin` ya no define `get_success_url`: la redirección la comparte el mixin común.

### Flujo completo de un envío válido

1. El navegador envía POST a la URL del formulario. Al no existir `action`, utiliza la misma dirección actual.
2. El middleware comprueba CSRF. Un token correcto no hace válidos los datos: son comprobaciones distintas.
3. La vista construye el ModelForm con los datos enviados.
4. Django valida tipos, campos, métodos `clean_*`, `clean` y las validaciones del modelo que correspondan.
5. Si el formulario es válido, llama a `form_valid`; cobros y reservas aplican sus reglas adicionales.
6. `SuccessMessageMixin.form_valid` llama primero a su `super().form_valid(form)`.
7. La vista de modelo guarda el objeto, lo asigna a `self.object`, calcula la URL y construye la respuesta de redirección.
8. El control vuelve a `SuccessMessageMixin`, que obtiene el mensaje y lo registra con `messages.success`.
9. Se devuelve HTTP 302. El navegador solicita con GET la URL `_update` del objeto.
10. La plantilla muestra el aviso de éxito y el formulario de actualización.

Este orden corrige una simplificación anterior: la respuesta de redirección se construye durante la llamada al padre; el mensaje se registra después del guardado y antes de devolver esa respuesta al navegador.

Si falla la validación, el formulario vuelve a mostrarse normalmente con HTTP 200. `form_invalid()` no deshace un guardado que ya se hubiera ejecutado: en nuestro flujo el rechazo ocurre antes del guardado. El formulario puede mostrar errores de campos; el mixin puede añadir un aviso general con `messages.error`.

## 6. FormHelper, constructor y layout: UD4.4.c

Los nueve formularios comparten este patrón, con un layout diferente:

```python
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_tag = False
    self.helper.layout = Layout(
        Row(
            Column('nombre', css_class='col-md-12'),
        ),
    )
```

`__init__` se ejecuta al construir el formulario, tanto vacío como con datos o con una instancia existente. `*args` y `**kwargs` transmiten esos argumentos al constructor padre. El padre crea los campos antes de que los organicemos.

`FormHelper()` contiene la configuración visual. `form_tag=False` evita que Crispy dibuje otro elemento `<form>`, pues la plantilla ya tiene uno. No desactiva la validación ni el token CSRF.

`Layout` agrupa la estructura; `Row` crea una fila y `Column` una columna. Los nombres como `'nombre'` se refieren a campos existentes del formulario. Bootstrap divide la fila en doce partes; `col-md-6` ocupa la mitad a partir del tamaño medio, y en pantallas menores el contenido puede apilarse.

El PDF muestra `FormHelper(self)` y `Div/Field`, mientras nuestra implementación usa `FormHelper()` con layout explícito y `Row/Column`. Son variantes funcionales; **Row/Column no aparece literalmente en el ejemplo del PDF**. Con el contrato estricto de usar solo lo explicado, debe justificarse mediante los enlaces que el profesor autorice o adaptarse al ejemplo `Div/Field`. No basta con afirmar que se ha copiado exactamente el mecanismo del ejemplo.

## 7. Plantilla común y CSRF: UD4.4.b

La plantilla carga `{% load crispy_forms_tags %}`, usa `<form method="post" novalidate>` y renderiza `{% crispy form %}`. Se eliminó la condición provisional que usaba `form.as_p` para formularios todavía sin helper. Los botones Crear/Actualizar y el enlace Eliminar siguen en la plantilla.

`novalidate` evita el bloqueo por la validación HTML nativa al enviar. Las comprobaciones del servidor permanecen activas. Crispy representa sus errores con estilos Bootstrap.

### Corrección de lo explicado anteriormente sobre el token

El estado real actual conserva `{% csrf_token %}` explícito y además Crispy genera otro token. La revisión contó **dos campos `csrfmiddlewaretoken` en cada una de las 18 pantallas**. No son dos formularios: cada pantalla contiene un único `<form>`.

La plantilla instalada `crispy_bootstrap5/templates/bootstrap5/whole_uni_form.html` incluye el token cuando el método es POST y `disable_csrf` no está activo, con independencia de `form_tag`. Por tanto, fue incorrecta la explicación anterior de que `form_tag=False` justificaba mantener el token explícito y que no estaba duplicado.

La página 30 del PDF pide retirar el token explícito porque Crispy ya lo genera. La propuesta pendiente es quitar esa línea solo de la plantilla de creación/actualización y volver a contar los tokens. La confirmación de borrado no utiliza Crispy y debe conservar su token. Esta revisión no aplica la corrección.

## 8. Distribución final: UD4.4.d y UD4.4.e

Los números indican columnas de Bootstrap. Esta tabla sirve como transcripción para completar el anexo del profesor.

| Formulario | Fila 1 | Fila 2 | Fila 3 |
|---|---|---|---|
| ClienteForm | nombre 3, apellidos 6, nif 3 | email 12 | telefono 6, activo 6 |
| FacturaForm | cliente 12 | numero 4, fecha 4, total 4 | concepto 12 |
| CobroForm | factura 12 | fecha 6, importe 6 | — |
| CategoriaServicioForm | nombre 4, descripcion 8 | — | — |
| ServicioForm | categoria 4, nombre 8 | descripcion 12 | duracion_minutos 4, precio 4, activo 4 |
| PeluqueroForm | nombre 6, apellidos 6 | email 6, telefono 6 | servicios 9, activo 3 |
| HorarioSemanalForm | peluquero 6, dia_semana 6 | hora_inicio 5, hora_fin 5, activo 2 | — |
| ExcepcionHorarioForm | peluquero 6, fecha 6 | hora_inicio 5, hora_fin 5, cerrado 2 | motivo 12 |
| ReservaForm | cliente 6, peluquero 6 | servicios 12 | fecha_inicio 6, estado 6 | 

Las filas de billing prescritas coinciden con el anexo. Teléfono y activo son campos adicionales del modelo de cliente y tienen una tercera fila propia. Se han definido seis layouts de core, superando el mínimo de cinco. La tabla original del ODT sigue pendiente de completar: documentarla aquí no modifica el archivo entregable.

Reserva excluye `fecha_fin`, `duracion_total_minutos` y `precio_total` porque los calcula `ReservaMixin`. `fecha_creacion` la rellena Django y no es editable. Es una excepción acordada durante el trabajo respecto al texto «todos los campos» del ODT; falta conformidad del profesor, no debe presentarse como aceptación ya recibida.

## 9. Preguntas para estudiar

1. **¿Qué hace Crispy?** Representa el formulario utilizando el helper, el layout y las plantillas Bootstrap.
2. **¿Quién valida?** El formulario y el modelo; las reglas adicionales de las vistas se comparten con mixins.
3. **¿Quién guarda?** En este flujo, CreateView/UpdateView mediante el ModelForm cuando se alcanza el `form_valid` del padre.
4. **¿Qué es context?** Un diccionario de datos que recibe la plantilla, no una página diferente.
5. **¿Cómo obtiene Crispy el formulario?** La vista lo entrega como `form` en el contexto.
6. **¿Para qué sirve `form_tag=False`?** Evita un `<form>` anidado; no elimina CSRF.
7. **¿Qué hace `reverse_lazy`?** Construye una URL por su nombre y argumentos; la redirección provoca la siguiente petición.
8. **¿Qué significa `{object}`?** Un marcador del mensaje que sustituimos por el objeto guardado.
9. **¿Por qué no hay dos mensajes de éxito al crear?** Solo se registra al guardar; el GET de destino representa el formulario sin repetir el guardado.
10. **¿Por qué nueve formularios y dieciocho vistas?** Cada pareja Create/Update comparte un formulario. El número 16 del ODT es una discrepancia pendiente de confirmar.
11. **¿Qué diferencia hay entre importe positivo y suma permitida?** Un pago de 30 es positivo, pero puede superar una factura si ya se han cobrado 80 de un total de 100.
12. **¿HTTP 200 prueba que todo funciona?** Solo prueba la respuesta de esa petición. No demuestra el comportamiento de todos los POST, el diseño en el navegador ni la ausencia de errores de datos incompletos.

## 10. Revisión final del conjunto UD4

### Evidencias ejecutadas el 16/11/2026

- `manage.py check`: sin incidencias.
- `manage.py makemigrations --check --dry-run`: ningún cambio pendiente de generar. No prueba por sí solo que todas las migraciones estén aplicadas en otros entornos.
- `pip check`: sin incompatibilidades declaradas.
- 36 peticiones GET: creación, actualización, confirmación y listado de los nueve modelos, todas HTTP 200.
- En las 18 pantallas de formulario: un `<form>`, todos los campos presentes una vez en el layout, destino `_update` correcto y mensaje que incluye el objeto. Dos tokens CSRF por pantalla: pendiente.
- Nueve listados comprobados con `ordering=asc` y `ordering=desc`: orden por identificador correcto. La pérdida inicial del parámetro al paginar quedó corregida y comprobada en una prueba posterior autorizada.
- Creación y actualización reales de una categoría temporal, dentro de una transacción revertida: ambas HTTP 302 y mensajes de éxito nivel 25 con su objeto. Comprobado que no queda la categoría de prueba.
- Cliente de pruebas con `enforce_csrf_checks=True`: POST sin token rechazado con HTTP 403; con token, operación válida.
- Formulario de horario activo con día vacío: se reprodujo inicialmente `RelatedObjectDoesNotExist`. Tras corregir la comprobación a `dia_semana_id is None`, crear y actualizar muestran el error obligatorio sin excepción. Los registros no cambian.

No se ha realizado en esta revisión un ciclo de guardado exitoso para los nueve modelos ni una inspección visual interactiva de todos los tamaños de pantalla. Las comprobaciones anteriores del chat sobre cobros y reservas son antecedentes, no nuevas pruebas exhaustivas en esta ejecución. No se otorga una nota automática ni se afirma ausencia total de fallos.

### Pendientes técnicos demostrados

| Prioridad | Hallazgo | Propuesta para la siguiente implementación autorizada |
|---|---|---|
| Resuelto | `HorarioSemanal.clean()` accedía a una relación vacía | Se comprueba `self.dia_semana_id is None`; POST incompletos de crear/actualizar verificados |
| Resuelto | Token CSRF duplicado en los formularios Crispy | Retirado el explícito; un token por pantalla y protección CSRF comprobada |
| Media | `messages.html` usa `data-dismiss="alert"` y `class="close"` con Bootstrap 5 | Ajustarlo al ejemplo del PDF: `data-bs-dismiss="alert"` y `btn-close`; verificar cierre en navegador |
| Resuelto | Los enlaces `?page=...` descartaban `ordering` | Ambos enlaces conservan asc/desc; sin parámetro o con otro valor no añaden ordering |

### Pendientes de trazabilidad académica

- **Comentarios UD4.3:** solo existen a, b y c en la rúbrica. La definición de todos los ModelForm corresponde a a; las validaciones positivas de Factura/Cobro a b; las tres validaciones de core a c. Los códigos actuales d–i de core y el c de `CobroForm.clean_importe()` no corresponden a esa rúbrica.
- **Comentarios UD4.4:** c identifica los constructores/helpers; d debe identificar los layouts de billing y e los layouts de core. Actualmente los layouts aparecen etiquetados solo como c. Revisar también la identificación de atributos de éxito en cada vista bajo a.
- **Anexos y explicaciones:** falta trasladar al ODT la tabla de vistas de core, las dos validaciones de reservas, las tres validaciones de formularios y los layouts de core. Esta guía y la autoevaluación Markdown aportan la transcripción, pero no rellenan los ODT originales.
- **Número de formularios:** hay nueve parejas de vistas, y nueve formularios. El ODT dice simultáneamente «uno por pareja» y «16». Es una inconsistencia pendiente de consulta, no una errata confirmada por el profesor.
- **Reserva:** documentar y confirmar la exclusión de campos derivados frente a «todos los campos».
- **Crispy:** justificar `Row/Column` y `FormHelper()` frente al ejemplo literal `Div/Field` y `FormHelper(self)`, o proponer la adaptación antes de hacerla.
- El ODT exige explicaciones originales y advierte sobre las copias. El alumno debe comprender el código, explicarlo con sus palabras y confirmar las condiciones de ayuda permitidas con su profesor. Una guía generada no demuestra por sí sola ese aprendizaje.

### Texto para los apartados explicativos del ODT

**UD4.2.h:** En las vistas de creación y actualización de reservas se reutiliza `ReservaMixin`, que llama a `validar_reserva`. Se comprueba que el profesional pueda realizar todos los servicios seleccionados y que la cita esté disponible. La disponibilidad exige un intervalo futuro, encajado en su horario o excepción, y sin solaparse con otra reserva. Al actualizar se excluye la propia reserva para no detectarla como conflicto.

**UD4.3.c:** Se valida que el precio del servicio sea positivo en `ServicioForm.clean_precio`, que la hora final sea posterior a la inicial en `HorarioSemanalForm.clean` y que la fecha de la excepción no sea pasada en `ExcepcionHorarioForm.clean_fecha`. Las dos últimas refuerzan reglas existentes del modelo; no son tres reglas nuevas de base de datos. El fallo de día vacío quedó corregido y comprobado posteriormente usando la clave de la relación en la comprobación previa.

**Anexo I, tabla 1, core:** Para CategoriaServicio, Servicio, Peluquero, HorarioSemanal, ExcepcionHorario y Reserva existen CreateView, UpdateView y DeleteView. Las dos primeras utilizan `common/base_create_update.html` y redirigen a su ruta `_update` con PK; DeleteView utiliza `common/base_confirm_delete.html`, hereda la protección común y vuelve a su ruta `_list`. Los prefijos son `categoria_servicio`, `servicio`, `peluquero`, `horario_semanal`, `excepcion_horario` y `reserva`. Sus campos y particularidades quedan definidos en los formularios enlazados en esta guía.

**UD4.4.e:** Se han diseñado los seis layouts de core de la tabla de la sección 8. Cada formulario crea su helper en `__init__`, evita un formulario HTML anidado y distribuye sus campos en filas de doce columnas. Reserva únicamente presenta los campos de entrada manual.

## 11. Orden de cierre recomendado

1. Completar la corrección pendiente de alertas. Horario vacío, CSRF y paginación ya están corregidos con autorización.
2. Corregir los códigos de comentarios conforme a la rúbrica y resolver las diferencias de material permitido.
3. Probar los errores y los ciclos de guardado afectados, y revisar el diseño en navegador.
4. Trasladar tablas y explicaciones a los documentos de entrega y confirmar con el profesor las excepciones.
5. Actualizar la autoevaluación con evidencias finales y guardar en Git cuando el alumno lo solicite.

La revisión inicial creó documentación y un diagnóstico temporal. Las correcciones posteriores de CSRF, horario vacío y paginación se aplicaron con autorización expresa. Los documentos originales del profesor siguen sin modificar.

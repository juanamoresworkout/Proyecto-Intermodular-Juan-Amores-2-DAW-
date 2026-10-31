# Autoevaluación de la UD3 Servidor

## Proyecto

- **Tema:** aplicación web de reservas.
- **Anteproyecto / Hito 1:** completado por el alumno antes de continuar con los siguientes bloques.
- **Estado actual revisado:** actividades UD3.2 completadas; modelos, administrador y migraciones de UD3.3-UD3.4 implementados; UD3.5 y UD3.6 pendientes de cerrar con todas sus evidencias.
- **Forma de trabajo:** implementación guiada paso a paso realizada por el alumno.
- **Criterio de revisión:** cada tarea solo se marcará como hecha cuando el código y su funcionamiento hayan sido comprobados.
- **Evidencias:** cuando una tarea requiera capturas, se anotarán aquí y se incorporarán después a la documentación.

## Convención obligatoria para los comentarios

Antes de cada fragmento creado para una tarea se añadirá un comentario con el código exacto y una explicación breve y original.

```python
# UD3.2.a: Aquí se crea y configura el entorno virtual del proyecto.
```

```html
<!-- UD3.8.a: Aquí se muestra la lista de reservas. -->
```

No se usarán comentarios genéricos ni copiados literalmente. El comentario debe explicar qué se ha implementado en ese fragmento.

## Seguimiento y calificación

> Estados posibles: `Pendiente`, `En proceso`, `Hecho` o `Necesita corrección`.
>
> La calificación queda sin asignar (`—`) hasta que exista una implementación revisable. Según la rúbrica, cada tarea obtiene toda su puntuación o 0 si no cumple todos los requisitos.

### UD3.1 Comentarios en el código — RA5.h

| Tarea | Requisito | Valor | Estado | Nota | Evidencia y revisión |
|---|---|---:|---|---:|---|
| UD3.1.a | Delimitar cada solución posterior con el código de tarea y un comentario explicativo en Python o HTML. | 10 | En proceso | — | Convención definida en este documento. Se comprobará durante todas las actividades. |

### UD3.2 Puesta a punto del proyecto Django — RA5.e

| Tarea | Requisito | Valor | Estado | Nota | Evidencia y revisión |
|---|---|---:|---|---:|---|
| UD3.2.a | Crear el entorno virtual `piapp-env` e instalar Django 5.2. | 1,5 | Hecho | 1,5 | Entorno creado con Python 3.13.14, Django 5.2.18 instalado y directorio `piapp-env/` correctamente ignorado por Git. |
| UD3.2.b | Crear un proyecto con un nombre identificable. | 1,5 | Hecho | 1,5 | Proyecto `reservas` creado en la raíz. Contiene `manage.py` y el paquete de configuración esperado; `manage.py check` no detecta problemas. |
| UD3.2.c | Crear un superusuario. | 1 | Hecho | 1 | Migraciones iniciales aplicadas, base de datos `db.sqlite3` creada y acceso al administrador confirmado por el alumno. No se registran credenciales. |
| UD3.2.d | Ejecutar la recolección de archivos estáticos y comprobar las carpetas. | 1 | Hecho | 1 | `STATIC_ROOT` configurado según la guía, `collectstatic` ejecutado y carpeta `static/admin` verificada. El resultado generado está ignorado por Git. |
| UD3.2.e | Aplicar en `settings.py` y `urls.py` los cambios de los apartados 5.1 y 5.3.3 de la teoría. | 1 | Hecho | 1 | Idioma, zona horaria, plantillas, estáticos y multimedia configurados; Pillow 13.0.0 instalado, `requirements.txt` generado y `manage.py check` superado. |
| UD3.2.f | Crear y registrar las apps `common`, `core` y `billing`. | 1,5 | Hecho | 1,5 | Las tres apps tienen la estructura estándar, están registradas mediante sus clases `AppConfig` y `manage.py check` no detecta problemas. |
| UD3.2.g | Crear `templates` y configurarla en `settings.py`. | 1 | Hecho | 1 | Carpeta global creada, configurada en `TEMPLATES['DIRS']` y 15 plantillas base cargadas correctamente por el motor de Django. Su adaptación funcional queda pendiente para UD3.7 y UD3.8. |
| UD3.2.h | Preparar el proyecto para ejecutarse con Docker. | 1,5 | Hecho | 1,5 | `Dockerfile`, `.dockerignore` y `compose.yaml` validados; contenedor en ejecución, migraciones aplicadas, puerto 8000 publicado, administrador accesible y comprobación de Django superada. |

#### Guía técnica del bloque UD3.2

##### UD3.2.a Entorno virtual y Django

- **Dónde está:** `piapp-env/`, en la raíz del repositorio. Está excluido de Git mediante `.gitignore`.
- **Qué hace:** mantiene aislados Python y los paquetes del proyecto; contiene Django 5.2.18.
- **Por qué lo hacemos:** evita mezclar dependencias globales con las del proyecto y permite reproducir el entorno.
- **Sugerencia:** al finalizar este bloque generaremos `requirements.txt` para guardar las versiones necesarias sin subir `piapp-env/`.

##### UD3.2.b Proyecto Django

- **Dónde está:** `manage.py` está en la raíz y la configuración está dentro de `reservas/`.
- **Qué hace `manage.py`:** ejecuta las órdenes administrativas usando `reservas.settings`.
- **Qué hace `reservas/settings.py`:** reúne la configuración global: apps, base de datos, idioma, zona horaria, plantillas y estáticos.
- **Qué hace `reservas/urls.py`:** contiene las rutas principales; actualmente solo publica `/admin/`.
- **Qué hacen `reservas/asgi.py` y `reservas/wsgi.py`:** permiten que distintos servidores ejecuten la aplicación.
- **Qué hace `reservas/__init__.py`:** identifica la carpeta como paquete de Python.
- **Sugerencia:** mantener aquí solo la configuración y desarrollar la funcionalidad en `common`, `core` y `billing`.

##### UD3.2.c Base de datos inicial y superusuario

- **Dónde está:** la base de datos local está en `db.sqlite3`, en la raíz. Este archivo está excluido de Git mediante `.gitignore`.
- **Qué hace `migrate`:** crea las tablas internas de Django para usuarios, permisos, sesiones y administración.
- **Qué hace `createsuperuser`:** crea una cuenta con permisos para acceder a `/admin/` y gestionar los datos del proyecto.
- **Por qué no se sube `db.sqlite3`:** contiene datos locales y puede contener cuentas de usuario; cada entorno debe crear su propia base de datos mediante migraciones.
- **Sugerencia:** no guardar contraseñas en código, documentación, commits ni capturas.

##### UD3.2.d Recolección de archivos estáticos

- **Dónde se configura:** `STATIC_ROOT` está en `reservas/settings.py` y apunta a `static/`, tal como indica la guía.
- **Dónde se genera:** `static/`, en la raíz; actualmente contiene los recursos del administrador en `static/admin/`.
- **Qué hace `collectstatic`:** copia en una sola ubicación los CSS, JavaScript, fuentes e imágenes de Django y de las apps para que un servidor pueda publicarlos.
- **Por qué se ignora:** la carpeta `/static/` de la raíz es un resultado generado que se puede reconstruir ejecutando `python manage.py collectstatic`.
- **Sugerencia:** versionar los archivos estáticos originales que creemos dentro de cada app, pero no la copia recopilada en la carpeta `/static/` raíz.

##### UD3.2.e Configuración general y multimedia

- **Dónde está:** la configuración se encuentra en `reservas/settings.py` y la publicación de multimedia durante el desarrollo en `reservas/urls.py`.
- **Qué se configuró:** español, zona horaria de Madrid, carpeta global de plantillas, rutas `/static/` y `/media/`, y sus correspondientes carpetas físicas.
- **Cómo funciona multimedia:** con `DEBUG=True`, las peticiones que comienzan por `/media/` se resuelven contra `MEDIA_ROOT` mediante las rutas añadidas en `urls.py`.
- **Dependencia:** Pillow 13.0.0 permite trabajar con `ImageField`; está registrada junto con Django 5.2.18 en `requirements.txt`.
- **Verificación:** `python manage.py check` finaliza sin errores ni advertencias.
- **Sugerencia:** en producción, usar variables de entorno para `SECRET_KEY` y `DEBUG`, y servir estáticos y multimedia mediante un servidor o almacenamiento especializado.

##### UD3.2.f Aplicaciones del proyecto

- **Dónde están:** `common/`, `core/` y `billing/` se encuentran en la raíz, al mismo nivel que `manage.py`.
- **Dónde se registran:** `reservas/settings.py`, dentro de `INSTALLED_APPS`, mediante `CommonConfig`, `CoreConfig` y `BillingConfig`.
- **Qué hace `common`:** agrupará utilidades compartidas y contendrá `actividadorm.py` en UD3.6; inicialmente queda sin funcionalidad propia.
- **Qué hace `core`:** contendrá los cinco modelos y la lógica específica de la aplicación de reservas.
- **Qué hace `billing`:** contendrá la parte guiada de clientes, facturas y cobros.
- **Verificación:** Django carga las tres configuraciones sin incidencias en `manage.py check`.
- **Sugerencia:** mantener cada funcionalidad en la app responsable y evitar convertir `common` en una carpeta de código sin una responsabilidad clara.

##### UD3.2.g Plantillas globales

- **Dónde están:** `templates/common/` contiene las bases y componentes compartidos; las plantillas funcionales se organizarán por app.
- **Dónde se configura:** `reservas/settings.py`, mediante `TEMPLATES[0]['DIRS']` apuntando a la carpeta global `templates/`.
- **Qué hace:** permite que Django localice plantillas compartidas y específicas de las apps desde una única raíz.
- **Verificación:** las 15 plantillas entregadas compilan con el motor de Django y `manage.py check` no detecta incidencias.
- **Adaptación pendiente:** los seis HTML de Cliente, Factura y Cobro deben ubicarse bajo `templates/billing/`; sus campos, enlaces y contenidos se completarán en UD3.7 y UD3.8.
- **Sugerencia:** conservar la herencia desde `common/base.html`, corregir el HTML del menú lateral y adaptar los componentes antiguos de Bootstrap cuando se trabajen las vistas.

##### UD3.2.h Ejecución con Docker

- **Dónde está:** `Dockerfile`, `.dockerignore` y `compose.yaml` están en la raíz del proyecto.
- **Qué hace `Dockerfile`:** construye una imagen Linux con Python 3.13, instala `requirements.txt`, copia el proyecto y define el arranque de Django.
- **Qué hace `.dockerignore`:** excluye del contexto de construcción el entorno virtual, Git, cachés, base de datos local, estáticos recopilados, multimedia y posibles archivos privados.
- **Qué hace `compose.yaml`:** construye el servicio `web`, aplica migraciones, inicia Django, comparte el proyecto con `/app` y publica el puerto 8000.
- **Verificación:** contenedor activo, migraciones al día, Django 5.2.18 iniciado en `0.0.0.0:8000`, acceso correcto a `/admin/` y `manage.py check` sin incidencias.
- **Sugerencia:** esta configuración es de desarrollo; para producción se sustituirá `runserver`, se desactivará `DEBUG` y se externalizarán secretos y almacenamiento.

### UD3.3 Capa de datos — RA6.b

| Tarea | Requisito | Valor | Estado | Nota | Evidencia y revisión |
|---|---|---:|---|---:|---|
| UD3.3.a | Implementar cinco modelos propios en `core` y los modelos `Cliente`, `Factura` y `Cobro` en `billing`; ejecutar migraciones. | 7 | Hecho | 7 | `billing` contiene Cliente, Factura y Cobro. `core` contiene seis modelos adaptados al proyecto: CategoriaServicio, Servicio, Peluquero, HorarioSemanal, ExcepcionHorario y Reserva. Migraciones creadas y aplicadas. El sexto modelo es una ampliación funcional del horario. |
| UD3.3.b | Implementar `__str__` en todos los modelos según la tabla y completar el criterio para `core`. | 2 | Hecho | 2 | Los modelos de `billing` respetan el anexo I y los de `core` muestran representaciones identificables; se han visto funcionando en el administrador. |
| UD3.3.c | Implementar las restricciones únicas indicadas y las necesarias en `core`. | 1 | Hecho | 1 | NIF, email y número de factura son únicos. Servicio, HorarioSemanal y ExcepcionHorario declaran `unique_together` en `Meta`; HorarioSemanal conserva además la restricción que exige que la hora final sea posterior. Migraciones `core.0003` y `core.0004` aplicadas. |

### UD3.4 Configuración del administrador — RA5.g

| Tarea | Requisito | Valor | Estado | Nota | Evidencia y revisión |
|---|---|---:|---|---:|---|
| UD3.4.a | Comentar en la misma línea el propósito de cada atributo de `ModelAdmin` la primera vez que aparezca. | 1 | Hecho | 1 | Los atributos se documentan en `ClienteAdmin`; los atributos nuevos `filter_horizontal` y `readonly_fields` también tienen comentario identificativo. |
| UD3.4.b | Implementar `ClienteAdmin`, `FacturaAdmin` y `CobroAdmin` según el anexo II. | 2 | Hecho | 2 | Las tres clases están registradas y configuradas. `CobroAdmin` busca por número de factura y nombre/apellidos del cliente, según la aclaración del anexo. |
| UD3.4.c | Implementar una clase `ModelAdmin` para cada modelo de `core`. | 5 | Hecho | 5 | Los seis modelos actuales de `core` tienen su propia clase `ModelAdmin`, incluido el modelo adicional ExcepcionHorario. |
| UD3.4.d | Configurar `verbose_name` en las apps. | 0,5 | Hecho | 0,5 | `common`, `core` y `billing` muestran nombres descriptivos mediante sus clases `AppConfig`. |
| UD3.4.e | Configurar `verbose_name` y `verbose_name_plural` en todos los modelos. | 0,75 | Hecho | 0,75 | Todos los modelos de `billing` y `core` tienen ambos nombres configurados en `Meta`. |
| UD3.4.f | Configurar `ordering` en todos los modelos. | 0,75 | Hecho | 0,75 | Los modelos guiados siguen el anexo II y los modelos propios tienen una ordenación coherente con el calendario y las listas. |

> **Aclaración del Anexo II para UD3.4.b:** en `CobroAdmin`, `search_fields` debe buscar por número de factura y por nombre y apellidos del cliente. No debe utilizar un campo `codigo`. Los recorridos ORM se ajustarán al nombre definitivo del campo de factura, por ejemplo `factura__numero`, `factura__cliente__nombre` y `factura__cliente__apellidos`.

### UD3.5 Introducción de datos — RA6.e

| Tarea | Requisito | Valor | Estado | Nota | Evidencia y revisión |
|---|---|---:|---|---:|---|
| UD3.5.a | Introducir datos de prueba desde el administrador y aportar una captura de la lista de cada modelo. | 10 | Hecho | 10 | Datos y capturas disponibles para los nueve modelos actuales. El alumno entregará juntas las capturas definitivas que desea incorporar al documento Word. |

### UD3.6 ORM de Django — RA6.c

| Tarea | Requisito | Valor | Estado | Nota | Evidencia y revisión |
|---|---|---:|---|---:|---|
| UD3.6.a | Crear `common/actividadorm.py` con los 20 métodos del anexo IV y probarlos en `python manage.py shell`. | 10 | En proceso | — | Los 20 métodos están implementados y contrastados con el anexo IV. Se corrigió la operación 17. Consta la ejecución en shell de la operación 1; falta conservar evidencia o confirmación individual de las restantes, especialmente las que modifican o eliminan datos. |

#### Operaciones ORM implementadas

1. `get_clientes_all`
2. `get_factura_first_3`
3. `get_factura_0`
4. `get_cliente_not_0612`
5. `get_cliente_dni_apellido`
6. `get_cli_id_lt_2_num_fact_des`
7. `get_cli_id_gt_2`
8. `get_fact_des_nom_des`
9. `get_fact_not_1`
10. `get_cobro_python_id2`
11. `get_cobro_fact6_not_manu`
12. `get_fact_gt_5`
13. `get_cobro_5_10`
14. `create_cliente`
15. `create_factura`
16. `update_last_factura`
17. `update_cobro_fact2_x2`
18. `update_cobro_fact1_cligonz_div2`
19. `delete_cobro_fact_lt_1`
20. `delete_cobro_cli_pablo`

### UD3.7 Programación de la aplicación — RA5.f

| Tarea | Requisito | Valor | Estado | Nota | Evidencia y revisión |
|---|---|---:|---|---:|---|
| UD3.7.a | Programar las vistas de `core` y completar la tabla de vistas del anexo III. | 5 | Hecho | 5 | Creadas las vistas de lista y detalle para CategoriaServicio, Servicio, Peluquero, HorarioSemanal, ExcepcionHorario y Reserva; se añadieron nombres de contexto explícitos en los modelos compuestos. |
| UD3.7.b | Crear las URLs de `core` y completar la tabla de URLs del anexo III. | 5 | Hecho | 5 | `core/urls.py` contiene doce rutas de lista y detalle con PK; el proyecto las incorpora bajo el prefijo `/reservas/` y el panel enlaza con los seis listados. |

### UD3.8 Publicación de los datos — RA6.d

| Tarea | Requisito | Valor | Estado | Nota | Evidencia y revisión |
|---|---|---:|---|---:|---|
| UD3.8.a | Crear las plantillas de `core` y completar la tabla de plantillas del anexo III. | 7 | Hecho | 7 | Creadas doce plantillas de lista y detalle para los seis modelos propios, con navegación, relaciones, estados, horarios y casos sin datos. |
| UD3.8.b | Implementar paginación en las vistas y plantillas de listas de `billing` y `core`. | 3 | Hecho | 3 | Las nueve `ListView` usan `paginate_by = 5` y reutilizan `common/pagination.html`. La navegación, el panel, el menú lateral, los listados y los detalles han sido comprobados manualmente por el alumno. |

## Registro de revisiones

| Fecha | Bloque | Resultado | Próxima mejora |
|---|---|---|---|
| 22/10/2026 | Estado inicial | Proyecto Django aún no iniciado; seguimiento creado. | Comenzar por UD3.1 y UD3.2.a. |
| 22/10/2026 | UD3.2.a | Django 5.2.18 instalado fuera del entorno virtual; `piapp-env` no existe. | Crear el entorno con `python -m venv piapp-env`, activarlo e instalar Django dentro de él. |
| 22/10/2026 | UD3.2.a | Corregido y verificado: entorno aislado con Python 3.13.14 y Django 5.2.18; exclusión de Git confirmada. Nota: 1,5/1,5. | Crear el proyecto Django de UD3.2.b. |
| 22/10/2026 | UD3.2.b | Proyecto `reservas` creado con la estructura correcta y sin incidencias en la comprobación de Django. Nota: 1,5/1,5. | Aplicar las migraciones iniciales y crear el superusuario de UD3.2.c. |
| 23/10/2026 | UD3.2.c | Base de datos inicial creada y acceso al administrador confirmado. Nota: 1/1. | Configurar y ejecutar la recolección de archivos estáticos de UD3.2.d. |
| 23/10/2026 | UD3.2.d | `STATIC_ROOT` configurado y contenido recopilado en `static/admin` según la guía. Nota: 1/1. | Aplicar la configuración indicada por la teoría en UD3.2.e. |
| 26/10/2026 | UD3.2.e | Configuración contrastada con la teoría; Django 5.2.18 y Pillow 13.0.0 verificados; `requirements.txt` reproducible y comprobación del sistema superada. Nota: 1/1. | Crear y registrar las apps `common`, `core` y `billing` de UD3.2.f. |
| 26/10/2026 | UD3.2.f | Apps `common`, `core` y `billing` creadas, registradas explícitamente y validadas. Nota: 1,5/1,5. | Crear y comprobar la carpeta global de plantillas de UD3.2.g. |
| 26/10/2026 | UD3.2.g | Carpeta global configurada y 15 plantillas base compiladas. Nota: 1/1. | Reorganizar y adaptar las plantillas durante UD3.7-UD3.8; preparar Docker en UD3.2.h. |
| 27/10/2026 | UD3.2.h | Imagen y servicio Docker validados; migraciones, servidor, estáticos del administrador y acceso autenticado comprobados. Nota: 1,5/1,5. | Confirmar los archivos Docker en Git y comenzar el diseño de modelos de UD3.3. |
| 30/10/2026 | UD3.3 | Modelos, representaciones, restricciones `unique_together` y migraciones comprobados. `manage.py check` finaliza sin incidencias. Nota: 10/10. | Conservar en Git las migraciones `core.0003` y `core.0004` como historial del cambio. |
| 30/10/2026 | UD3.4 | Administradores, nombres visibles y ordenaciones revisados. Nota: 10/10. | Conservar las capturas y completar la tabla propia del anexo II en la documentación final. |
| 30/10/2026 | UD3.5 | Datos y capturas de los nueve modelos confirmados por el alumno. Nota: 10/10. | Incorporar al Word únicamente las capturas definitivas que entregue el alumno. |
| 30/10/2026 | UD3.6 | Los 20 métodos ORM están escritos y revisados respecto al anexo IV; operación 17 corregida. | Registrar la ejecución en `manage.py shell` de las operaciones restantes sin repetir innecesariamente las operaciones destructivas. |
| 31/10/2026 | UD3.7 | Vistas y rutas de lista y detalle terminadas para `billing` y los seis modelos propios de `core`. Nota: 10/10. | Conservar una captura del panel y de la navegación entre lista y detalle para el documento final. |
| 31/10/2026 | UD3.8 | Plantillas de `core` y paginación común terminadas. Nota: 10/10. | Obtener una captura de la paginación cuando un listado tenga más de cinco registros. |
| 31/10/2026 | UD3.7-UD3.8 | Comprobación manual final correcta: panel, menú lateral, nueve listados, rutas de detalle y paginación operativos. | Guardar las capturas definitivas para completar el documento de actividades. |

## Registro de capturas pendientes

| Código | Captura necesaria | Estado | Ubicación final |
|---|---|---|---|
| UD3.5.a | Listas del administrador de los nueve modelos actuales. | Disponibles; pendiente recibir la selección definitiva del alumno. | Documento Word final de actividades. |


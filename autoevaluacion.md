# Autoevaluación de la UD3 Servidor

## Proyecto

- **Tema:** aplicación web de reservas.
- **Estado inicial revisado:** repositorio con `README.md` y `LICENSE`; el proyecto Django todavía no está creado.
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
| UD3.2.a | Crear el entorno virtual `piapp-env` e instalar Django 5.2. | 1,5 | Necesita corrección | — | Django 5.2.18 está instalado para el usuario, pero `piapp-env` no se creó porque esta instalación no incluye el lanzador `py`. Repetir usando `python -m venv`. |
| UD3.2.b | Crear un proyecto con un nombre identificable. | 1,5 | Pendiente | — | Revisar la estructura creada. |
| UD3.2.c | Crear un superusuario. | 1 | Pendiente | — | Comprobar acceso al administrador sin registrar credenciales. |
| UD3.2.d | Ejecutar la recolección de archivos estáticos y comprobar las carpetas. | 1 | Pendiente | — | Revisar salida y directorios generados. |
| UD3.2.e | Aplicar en `settings.py` y `urls.py` los cambios de los apartados 5.1 y 5.3.3 de la teoría. | 1 | Pendiente | — | Comparar configuración con la guía. |
| UD3.2.f | Crear y registrar las apps `common`, `core` y `billing`. | 1,5 | Pendiente | — | Revisar apps e `INSTALLED_APPS`. |
| UD3.2.g | Crear `templates` y configurarla en `settings.py`. | 1 | Pendiente | — | Comprobar búsqueda de plantillas. |
| UD3.2.h | Preparar el proyecto para ejecutarse con Docker. | 1,5 | Pendiente | — | Revisar archivos y ejecución del contenedor. |

### UD3.3 Capa de datos — RA6.b

| Tarea | Requisito | Valor | Estado | Nota | Evidencia y revisión |
|---|---|---:|---|---:|---|
| UD3.3.a | Implementar cinco modelos propios en `core` y los modelos `Cliente`, `Factura` y `Cobro` en `billing`; ejecutar migraciones. | 7 | Pendiente | — | Los cinco modelos de reservas se decidirán antes de implementarlos. |
| UD3.3.b | Implementar `__str__` en todos los modelos según la tabla y completar el criterio para `core`. | 2 | Pendiente | — | Comprobar representaciones en shell y administrador. |
| UD3.3.c | Implementar las restricciones únicas indicadas y las necesarias en `core`. | 1 | Pendiente | — | Revisar `Meta`, migraciones e integridad. |

### UD3.4 Configuración del administrador — RA5.g

| Tarea | Requisito | Valor | Estado | Nota | Evidencia y revisión |
|---|---|---:|---|---:|---|
| UD3.4.a | Comentar en la misma línea el propósito de cada atributo de `ModelAdmin` la primera vez que aparezca. | 1 | Pendiente | — | Revisar claridad y códigos de tarea. |
| UD3.4.b | Implementar `ClienteAdmin`, `FacturaAdmin` y `CobroAdmin` según el anexo II. | 2 | Pendiente | — | 0,5 + 0,75 + 0,75 puntos. |
| UD3.4.c | Implementar una clase `ModelAdmin` para cada modelo de `core`. | 5 | Pendiente | — | Un punto por cada uno de los cinco modelos. |
| UD3.4.d | Configurar `verbose_name` en las apps. | 0,5 | Pendiente | — | Revisar `apps.py`. |
| UD3.4.e | Configurar `verbose_name` y `verbose_name_plural` en todos los modelos. | 0,75 | Pendiente | — | Revisar la clase `Meta`. |
| UD3.4.f | Configurar `ordering` en todos los modelos. | 0,75 | Pendiente | — | Comparar con el anexo II y los criterios propios de `core`. |

### UD3.5 Introducción de datos — RA6.e

| Tarea | Requisito | Valor | Estado | Nota | Evidencia y revisión |
|---|---|---:|---|---:|---|
| UD3.5.a | Introducir datos de prueba desde el administrador y aportar una captura de la lista de cada modelo. | 10 | Pendiente | — | **Capturas obligatorias:** una por cada uno de los ocho modelos, 1,25 puntos cada una. |

### UD3.6 ORM de Django — RA6.c

| Tarea | Requisito | Valor | Estado | Nota | Evidencia y revisión |
|---|---|---:|---|---:|---|
| UD3.6.a | Crear `common/actividadorm.py` con los 20 métodos del anexo IV y probarlos en `python manage.py shell`. | 10 | Pendiente | — | Cada operación vale 0,5 puntos; se revisarán individualmente. |

#### Operaciones ORM pendientes

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
| UD3.7.a | Programar las vistas de `core` y completar la tabla de vistas del anexo III. | 5 | Pendiente | — | Revisar modelo, clase y plantilla asociada. |
| UD3.7.b | Crear las URLs de `core` y completar la tabla de URLs del anexo III. | 5 | Pendiente | — | Revisar nombres, rutas, vistas y parámetros. |

### UD3.8 Publicación de los datos — RA6.d

| Tarea | Requisito | Valor | Estado | Nota | Evidencia y revisión |
|---|---|---:|---|---:|---|
| UD3.8.a | Crear las plantillas de `core` y completar la tabla de plantillas del anexo III. | 7 | Pendiente | — | Revisar listas y detalles de los cinco modelos. |
| UD3.8.b | Implementar paginación en las vistas y plantillas de listas de `billing` y `core`. | 3 | Pendiente | — | Comprobar navegación con suficientes registros. |

## Registro de revisiones

| Fecha | Bloque | Resultado | Próxima mejora |
|---|---|---|---|
| 22/10/2026 | Estado inicial | Proyecto Django aún no iniciado; seguimiento creado. | Comenzar por UD3.1 y UD3.2.a. |
| 22/10/2026 | UD3.2.a | Django 5.2.18 instalado fuera del entorno virtual; `piapp-env` no existe. | Crear el entorno con `python -m venv piapp-env`, activarlo e instalar Django dentro de él. |

## Registro de capturas pendientes

| Código | Captura necesaria | Estado | Ubicación final |
|---|---|---|---|
| UD3.5.a | Lista del administrador para cada modelo de `billing` y `core`. | Pendiente | Documentación del proyecto, por decidir. |


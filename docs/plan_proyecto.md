# Plan integrado del proyecto de reservas

## Propósito

Este documento une las actividades de Servidor UD3 con el anteproyecto y los requisitos generales del Proyecto Intermodular. Se actualizará conforme se completen y verifiquen tareas.

## Fuentes de requisitos

- Anteproyecto: https://jpaniorte.github.io/2daw-daw-2627/proyectos/anteproyecto/
- Normativa general: https://github.com/jpaniorte/2daw-tfc-2627/wiki
- Requisitos de Despliegue: https://github.com/jpaniorte/2daw-tfc-2627/wiki/Despliegue-de-Aplicaciones-Web
- Actividades UD3 de Servidor y sus anexos.
- Tablero de ClickUp del alumno.

## Propuesta actual

- **Título provisional:** Sistema web de reservas.
- **Autor:** Juan Amores.
- **Descripción:** aplicación web para consultar disponibilidad y crear, consultar o cancelar reservas, con una zona privada de administración para gestionar los recursos reservables, los servicios, la disponibilidad, las reservas, los clientes, las facturas y los cobros.
- **Problema que resuelve:** centraliza la disponibilidad y evita gestionar reservas, clientes y cobros mediante procesos separados o manuales.
- **Temática:** gestión de reservas y administración de servicios.
- **Backend:** Python 3.13 y Django 5.2.
- **Frontend:** React, según la propuesta recogida en el README.
- **Base de datos inicial:** SQLite durante los ejercicios; PostgreSQL en la evolución del proyecto y el despliegue.
- **Contenedores:** Docker y Docker Compose.
- **Despliegue obligatorio:** AWS, al menos en una instancia EC2, con IP elástica, SSH y HTTPS.
- **Infraestructura como código:** Terraform o AWS CloudFormation.
- **Despliegue continuo:** GitHub Actions o Jenkins.

La referencia visual de ClickUp que menciona Flutter y Laravel se interpreta como un ejemplo de planificación. Para este repositorio se adaptarán esas tareas al stack real React y Django, salvo que el profesor solicite expresamente otro stack.

## Objetivos

1. Permitir consultar recursos o servicios disponibles.
2. Permitir crear y cancelar reservas con control de disponibilidad.
3. Mantener separados los módulos de reservas y facturación.
4. Proporcionar una zona de administración accesible solo a usuarios con el rol adecuado.
5. Gestionar clientes, facturas y cobros.
6. Ofrecer una interfaz web responsive mediante React.
7. Documentar una API y demostrar la comunicación entre frontend y backend.
8. Ejecutar el proyecto localmente mediante Docker Compose.
9. Desplegar la aplicación en AWS con HTTPS e infraestructura reproducible.
10. Mantener documentación, bitácora y evidencias suficientes para que otra persona pueda reproducir el proyecto.

## Orden de trabajo acordado

### Decisión de secuencia del 27 de octubre de 2026

1. Completar los ejercicios backend hasta UD3.6 inclusive.
2. Cumplimentar el anteproyecto en ClickUp con la propuesta y el esquema E/R.
3. Presentar el anteproyecto y atender las correcciones del profesorado.
4. Decidir la siguiente fase después del visto bueno.

Hasta llegar a esa decisión no se implementará React, la landing page, la integración frontend-backend ni el despliegue AWS. Las actividades UD3.7 y UD3.8 también quedarán en espera tras finalizar UD3.6, salvo que el profesor indique otro orden.

### Fase 0 Preparación del anteproyecto

- [ ] Completar en ClickUp el título, autor, descripción, problema, objetivos, temática y tecnologías.
- [ ] Diseñar el esquema E/R inicial.
- [ ] Invitar al profesor al espacio de ClickUp.
- [ ] Añadir el enlace de ClickUp al README.
- [ ] Presentar el anteproyecto al terminar UD3.6 y obtener el visto bueno antes de continuar con las fases posteriores.

### Fase 1 Ejercicios de backend UD3

- [x] UD3.1 Convención de comentarios por código de tarea.
- [x] UD3.2 Preparación del proyecto Django.
- [ ] UD3.3 Modelos y migraciones.
- [ ] UD3.4 Administrador de Django.
- [ ] UD3.5 Datos de prueba y capturas.
- [ ] UD3.6 Operaciones ORM.
- [ ] **Punto de parada:** cumplimentar y presentar el anteproyecto.
- [ ] UD3.7 Vistas y URLs, pendiente de la decisión posterior.
- [ ] UD3.8 Plantillas y paginación, pendiente de la decisión posterior.

Los ejercicios guiados de `billing` se implementarán exactamente según los anexos. Los cinco modelos de `core` se definirán a partir del esquema E/R aprobado para el sistema de reservas.

### Fase 2 Estructura completa del repositorio

- [ ] Decidir con el profesor si el Django académico permanece en la raíz o pasa a `backend/`.
- [ ] Preparar el scaffold del backend Django para despliegue.
- [ ] Crear el scaffold del frontend React.
- [ ] Crear `docs/` y mantener la documentación técnica.
- [ ] Crear `.env.example` sin secretos.
- [ ] Crear `AGENTS.md` adaptado al stack y a las normas del repositorio.
- [ ] Crear o comprobar la rama `develop` y trabajar con ramas `feature/...`.

### Fase 3 Integración local

- [x] Docker Compose inicial para Django.
- [ ] Ampliar Compose con frontend y base de datos PostgreSQL.
- [ ] Crear un endpoint de salud o prueba en el backend.
- [ ] Consumir el endpoint desde React.
- [ ] Documentar los endpoints, preferentemente con una colección Bruno versionada en `docs/bruno/`.
- [ ] Actualizar el README con instrucciones reproducibles desde cero.

### Fase 4 Landing page y diseño

- [ ] Crear una landing page pública con descripción, beneficios principales y acceso a la aplicación.
- [ ] Preparar un diseño o prototipo y publicar su URL.
- [ ] Publicar la landing page y añadir su URL al README.
- [ ] Añadir un tutorial de uso con capturas o material multimedia.

La landing page podrá ser la ruta pública inicial del frontend React. La zona de administración y gestión permanecerá protegida por autenticación y rol.

### Fase 5 Despliegue

- [ ] Preparar una instancia AWS EC2 con acceso SSH e IP elástica.
- [ ] Desplegar servidor web, aplicación y base de datos según la arquitectura aprobada.
- [ ] Configurar HTTPS.
- [ ] Describir la infraestructura mediante Terraform o AWS CloudFormation.
- [ ] Implementar un pipeline con GitHub Actions o Jenkins.
- [ ] Valorar requisitos adicionales: RDS, balanceador, Route 53, WAF y SFTP.

### Fase 6 Checkpoint y entrega final

- [ ] Mantener código y README actualizados semanalmente.
- [ ] Mantener bitácora, bibliografía e histórico de cambios.
- [ ] Preparar un vídeo de checkpoint de cinco minutos como máximo.
- [ ] Preparar presentación final en PDF.
- [ ] Documentar dificultades, mejoras y conclusiones.
- [ ] Preparar una demostración breve para la exposición.

## Entregables documentales finales

- README reproducible con enlaces a ClickUp, landing page, diseño y despliegue.
- Documento Word de actividades UD3 completado.
- Documento Word de autoevaluación completado.
- Esquema E/R y tablas de los anexos rellenadas.
- Documento de instalación y configuración.
- Tutorial de uso con capturas.
- Bitácora de tareas.
- Bibliografía.
- Presentación final en PDF.

## Próxima decisión

Antes de implementar UD3.3 se debe cerrar el esquema E/R y confirmar los cinco modelos de `core`. La parte `billing` está fijada por el anexo; la parte de reservas debe coincidir con el anteproyecto aprobado.

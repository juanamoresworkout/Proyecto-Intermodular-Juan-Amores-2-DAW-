# Sistema de reservas para peluquería

Proyecto Django para gestionar clientes, servicios, peluqueros, horarios,
excepciones, reservas, facturas y cobros.

## Requisitos

- Python 3.13
- Docker Desktop, únicamente si se utiliza el arranque con Docker

## Arranque local desde cero

En PowerShell, situarse en la carpeta del proyecto y ejecutar:

```powershell
python -m venv piapp-env
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\piapp-env\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

La aplicación quedará disponible en:

```text
http://127.0.0.1:8000/
```

El administrador estará en:

```text
http://127.0.0.1:8000/admin/
```

La base de datos `db.sqlite3` no se entrega. Se reconstruye mediante las
migraciones y comienza vacía. Los datos se pueden introducir desde el
administrador de Django.

## Arranque con Docker

Con Docker Desktop iniciado:

```powershell
docker compose up --build
```

Para crear el superusuario dentro del contenedor:

```powershell
docker compose exec web python manage.py createsuperuser
```

Para detener el servicio:

```powershell
docker compose down
```

## Comprobaciones útiles

```powershell
python manage.py check
python manage.py showmigrations
```

## Estructura principal

- `reservas/`: configuración general del proyecto.
- `core/`: servicios, peluqueros, horarios, excepciones y reservas.
- `billing/`: clientes, facturas y cobros.
- `common/`: utilidades compartidas y ejercicios ORM.
- `templates/`: plantillas comunes y de las aplicaciones.
- `docs/`: documentación técnica del proyecto.

## Documentación del proyecto

- [Espacio del proyecto en ClickUp](https://app.clickup.com/1500510000002061/v/l/1ampjurgd0d-372)
- [Anteproyecto](https://app.clickup.com/t/1500510000002061/1ampjurh80m)

from billing.models import Cliente, Factura, Cobro

from datetime import timedelta

from django.utils import timezone



# UD3.6.a: Operación 1. Devuelve todos los clientes.
def get_clientes_all():
    return Cliente.objects.all()

# UD3.6.a: Operación 2. Devuelve las tres primeras facturas.
def get_factura_first_3():
    return Factura.objects.all()[:3]

# UD3.6.a: Operación 3. Devuelve las facturas cuyo total es cero.
def get_factura_0():
    return Factura.objects.filter(total=0)

# UD3.6.a: Operación 4. Excluye los clientes cuyo NIF empieza por 74.
def get_cliente_not_0612():
    return Cliente.objects.exclude(nif__startswith='74')

# UD3.6.a: Operación 5. Busca por NIF exacto y por parte de los apellidos.
def get_cliente_dni_apellido():
    return Cliente.objects.filter(
        nif='92436593F',
        apellidos__contains='Pérez',
    )

# UD3.6.a: Operación 6. Filtra facturas por ID y ordena por número descendente.
def get_cli_id_lt_2_num_fact_des():
    return Factura.objects.filter(
        id__lt=2,
    ).order_by('-numero')

# UD3.6.a: Operación 7. Devuelve los clientes cuyo ID es mayor que 2.
def get_cli_id_gt_2():
    return Cliente.objects.filter(id__gt=2)

# UD3.6.a: Operación 8. Busca PHP en el concepto y ordena por número ascendente.
def get_fact_des_nom_des():
    return Factura.objects.filter(
        concepto__contains='PHP',
    ).order_by('numero')

# UD3.6.a: Operación 9. Excluye las facturas cuyo número termina en 1.
def get_fact_not_1():
    return Factura.objects.exclude(numero__endswith='1')

# UD3.6.a: Operación 10. Devuelve el primer cobro que cumple ambas condiciones.
def get_cobro_python_id2():
    return Cobro.objects.filter(
        factura__concepto__contains='python',
        id__endswith='2',
    ).first()

# UD3.6.a: Operación 11. Busca cobros por factura y excluye clientes por nombre.
def get_cobro_fact6_not_manu():
    return Cobro.objects.filter(
        factura__numero__contains='06',
    ).exclude(
        factura__cliente__nombre__contains='Manu',
    )

# UD3.6.a: Operación 12. Devuelve las facturas con total mayor o igual que 5.
def get_fact_gt_5():
    return Factura.objects.filter(total__gte=5)

# UD3.6.a: Operación 13. Devuelve los cobros con importe entre 5 y 10.
def get_cobro_5_10():
    #Equivale a return Cobro.objects.filter(importe__gte=5,  importe__lte=10,)
    return Cobro.objects.filter(importe__range=(5, 10))

# UD3.6.a: Operación 14. Crea y devuelve un cliente.
#Incluye el cliente porque mi modelo lo exige.
def create_cliente():
    return Cliente.objects.create(
        nombre='Nuevo',
        apellidos='apellido1 apellido2',
        nif='00000000T',
        email='nuevo@example.com',
    )

# UD3.6.a: Operación 15. Crea una factura de ayer para el cliente anterior.
def create_factura():
    cliente = Cliente.objects.get(nif='00000000T')

    return Factura.objects.create(
        cliente=cliente,
        numero='F-2026-002',
        concepto='Factura del ejercicio ORM',
        fecha=timezone.localdate() - timedelta(days=1),
        total=100,
    )

# UD3.6.a: Operación 16. Añade "(última)" al concepto de la última factura.
def update_last_factura():
    factura = Factura.objects.last()

    if factura:
        factura.concepto += ' (última)'
        factura.save()

# UD3.6.a: Operación 17. Duplica los cobros de facturas terminadas en 2.
def update_cobro_fact2_x2():
    cobros = Cobro.objects.filter(
        factura__numero__endswith='2',
    )
    for cobro in cobros:
        cobro.importe *= 2 
        cobro.save()

# UD3.6.a: Operación 18. Divide entre dos los cobros que cumplen ambas condiciones.
def update_cobro_fact1_cligonz_div2():
    cobros = Cobro.objects.filter(
        factura__numero__endswith='1',
        factura__cliente__apellidos__contains='González',
    )

    for cobro in cobros:
        cobro.importe /= 2
        cobro.save()

# UD3.6.a: Operación 19. Elimina los cobros de facturas con total menor que 1.
def delete_cobro_fact_lt_1():
    return Cobro.objects.filter(
        factura__total__lt=1,
    ).delete()

# UD3.6.a: Operación 20. Elimina los cobros de clientes cuyo nombre contiene Pablo.
def delete_cobro_cli_pablo():
    return Cobro.objects.filter(
        factura__cliente__nombre__contains='Pablo',
    ).delete()


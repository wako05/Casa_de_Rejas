from db import SessionLocal, Inventario, Venta, init_db
import datetime
from sqlalchemy.orm import joinedload

init_db()

def agregar_producto(nombre, precios, precio_compra, stock, stock_minimo):
    session = SessionLocal()
    # Verificar si ya existe un producto con el mismo nombre
    existente = session.query(Inventario).filter(Inventario.nombre == nombre).first()
    if existente:
        session.close()
        return False  # Indica que ya existe
    prod = Inventario(
        nombre=nombre,
        caja_caliente=precios.get("Caja Caliente", 0),
        caja_fria=precios.get("Caja Fria", 0),
        particular=precios.get("Particular", 0),
        six_pack=precios.get("Six Pack", 0),
        unitario=precios.get("Unitario", 0),
        precio_compra=precio_compra,
        stock=stock,
        stock_minimo=stock_minimo
    )
    session.add(prod)
    session.commit()
    session.close()
    return True  # Indica éxito

def obtener_inventario():
    session = SessionLocal()
    productos = session.query(Inventario).all()
    session.close()
    return productos

def actualizar_stock(producto_id, nuevo_stock):
    session = SessionLocal()
    prod = session.query(Inventario).get(producto_id)
    if prod:
        prod.stock = nuevo_stock
        session.commit()
    session.close()

def registrar_venta(producto_id, tipo_precio, cantidad, descuento):
    session = SessionLocal()
    prod = session.query(Inventario).get(producto_id)
    precio = getattr(prod, tipo_precio.lower().replace(" ", "_"))
    valor_total = (precio * cantidad) - descuento
    venta = Venta(
        fecha=datetime.date.today(),
        producto_id=producto_id,
        tipo_precio=tipo_precio,
        cantidad=cantidad,
        valor_unitario=precio,
        valor_total=valor_total,
        descuento=descuento
    )
    prod.stock -= cantidad
    session.add(venta)
    session.commit()
    session.close()

def obtener_ventas():
    session = SessionLocal()
    ventas = session.query(Venta).options(joinedload(Venta.producto)).all()
    # Accede a los atributos necesarios antes de cerrar la sesión
    ventas_data = []
    for v in ventas:
        ventas_data.append({
            "fecha": v.fecha,
            "producto_nombre": v.producto.nombre if v.producto else "",
            "tipo_precio": v.tipo_precio,
            "cantidad": v.cantidad,
            "valor_unitario": v.valor_unitario,
            "valor_total": v.valor_total,
            "descuento": v.descuento
        })
    session.close()
    return ventas_data

def editar_stock(producto_id, nuevo_stock):
    session = SessionLocal()
    prod = session.query(Inventario).get(producto_id)
    if prod:
        prod.stock = nuevo_stock
        session.commit()
    session.close()

def editar_stock_y_minimo(producto_id, nuevo_stock, nuevo_stock_minimo):
    session = SessionLocal()
    prod = session.query(Inventario).get(producto_id)
    if prod:
        prod.stock = nuevo_stock
        prod.stock_minimo = nuevo_stock_minimo
        session.commit()
    session.close()

def obtener_stock_actual():
    session = SessionLocal()
    productos = session.query(Inventario).all()
    ventas = session.query(Venta).all()
    stock_actual = {}
    for prod in productos:
        vendidos = sum(v.cantidad for v in ventas if v.producto_id == prod.id)
        stock_actual[prod.id] = {
            "nombre": prod.nombre,
            "stock_inicial": prod.stock,
            "vendidos": vendidos,
            "stock_actual": prod.stock - vendidos
        }
    session.close()
    return stock_actual

def reemplazar_producto(nombre, precios, precio_compra, stock, stock_minimo):
    session = SessionLocal()
    prod = session.query(Inventario).filter(Inventario.nombre == nombre).first()
    if prod:
        prod.caja_caliente = precios.get("Caja Caliente", 0)
        prod.caja_fria = precios.get("Caja Fria", 0)
        prod.particular = precios.get("Particular", 0)
        prod.six_pack = precios.get("Six Pack", 0)
        prod.unitario = precios.get("Unitario", 0)
        prod.precio_compra = precio_compra
        prod.stock = stock
        prod.stock_minimo = stock_minimo
        session.commit()
    session.close()

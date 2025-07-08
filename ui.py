import streamlit as st
from main import agregar_producto, obtener_inventario, actualizar_stock, registrar_venta, obtener_ventas, editar_stock_y_minimo, obtener_stock_actual, reemplazar_producto
import pandas as pd
import io


st.set_page_config(page_title="Casa de Rejas", layout="wide")

tabs = st.tabs(["Inventario", "Ventas", "Stock actual"])

with tabs[0]:
    st.header("Inventario")
    with st.form("Agregar producto"):
        nombre = st.text_input("Nombre del producto")
        precios = {
            "Caja Caliente": st.number_input("Precio Caja Caliente", min_value=0.0),
            "Caja Fria": st.number_input("Precio Caja Fria", min_value=0.0),
            "Particular": st.number_input("Precio Particular", min_value=0.0),
            "Six Pack": st.number_input("Precio Six Pack", min_value=0.0),
            "Unitario": st.number_input("Precio Unitario", min_value=0.0)
        }
        precio_compra = st.number_input("Precio de compra", min_value=0.0)
        stock = st.number_input("Stock actual", min_value=0, step=1)
        stock_minimo = st.number_input("Stock mínimo", min_value=0, step=1)
        submitted = st.form_submit_button("Agregar")
        if submitted:
            resultado = agregar_producto(nombre, precios, precio_compra, stock, stock_minimo)
            if resultado is True:
                st.success("Producto agregado")
            else:
                st.warning("¡El producto ya existe!")

    productos = obtener_inventario()
    df = pd.DataFrame([{
        "ID": p.id,
        "Nombre": p.nombre,
        "Caja Caliente": p.caja_caliente,
        "Caja Fria": p.caja_fria,
        "Particular": p.particular,
        "Six Pack": p.six_pack,
        "Unitario": p.unitario,
        "Precio Compra": p.precio_compra,
        "Stock": p.stock,
        "Stock Mínimo": p.stock_minimo,
        "Alarma": "⚠️" if p.stock < p.stock_minimo else ""
    } for p in productos])
    st.dataframe(df)
    # Botón para descargar Excel directamente por el navegador
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False, engine='openpyxl')
    excel_buffer.seek(0)
    st.download_button(
        label="Descargar Inventario en Excel",
        data=excel_buffer,
        file_name="inventario.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="download_inventario"
    )

    # Nueva sección: Actualizar Datos
    st.subheader("Actualizar Datos")
    prod_nombres = [p.nombre for p in productos]
    if prod_nombres:
        prod_sel = st.selectbox("Selecciona producto a actualizar", prod_nombres, key="actualizar_datos")
        prod_obj = next((p for p in productos if p.nombre == prod_sel), None)
        if prod_obj:
            nuevo_stock = st.number_input("Nuevo stock", min_value=0, value=prod_obj.stock, step=1, key="nuevo_stock_actualizar")
            nuevo_stock_minimo = st.number_input("Nuevo stock mínimo", min_value=0, value=prod_obj.stock_minimo, step=1, key="nuevo_stock_minimo_actualizar")
            nuevo_precio_compra = st.number_input("Nuevo precio de compra", min_value=0.0, value=prod_obj.precio_compra, key="nuevo_precio_compra_actualizar")
            nuevo_caja_caliente = st.number_input("Nuevo precio Caja Caliente", min_value=0.0, value=prod_obj.caja_caliente, key="nuevo_caja_caliente_actualizar")
            nuevo_caja_fria = st.number_input("Nuevo precio Caja Fria", min_value=0.0, value=prod_obj.caja_fria, key="nuevo_caja_fria_actualizar")
            nuevo_particular = st.number_input("Nuevo precio Particular", min_value=0.0, value=prod_obj.particular, key="nuevo_particular_actualizar")
            nuevo_six_pack = st.number_input("Nuevo precio Six Pack", min_value=0.0, value=prod_obj.six_pack, key="nuevo_six_pack_actualizar")
            nuevo_unitario = st.number_input("Nuevo precio Unitario", min_value=0.0, value=prod_obj.unitario, key="nuevo_unitario_actualizar")
            if st.button("Actualizar datos", key="actualizar_datos_btn"):
                nuevos_precios = {
                    "Caja Caliente": nuevo_caja_caliente,
                    "Caja Fria": nuevo_caja_fria,
                    "Particular": nuevo_particular,
                    "Six Pack": nuevo_six_pack,
                    "Unitario": nuevo_unitario
                }
                # Usamos reemplazar_producto para actualizar todos los datos
                reemplazar_producto(
                    prod_obj.nombre,
                    nuevos_precios,
                    nuevo_precio_compra,
                    nuevo_stock,
                    nuevo_stock_minimo
                )
                st.success("Datos del producto actualizados correctamente")

with tabs[1]:
    st.header("Ventas")
    productos = obtener_inventario()
    prod_dict = {p.nombre: p for p in productos}
    prod_nombres = list(prod_dict.keys())
    with st.form("Registrar venta"):
        producto_sel = st.selectbox("Producto", prod_nombres)
        tipo_precio = st.selectbox("Tipo de precio", ["Caja Caliente", "Caja Fria", "Particular", "Six Pack", "Unitario"])
        cantidad = st.number_input("Cantidad", min_value=1, step=1)
        descuento = st.number_input("Descuento (entero)", min_value=0, step=1)
        precio_unitario = getattr(prod_dict[producto_sel], tipo_precio.lower().replace(" ", "_"))
        st.write(f"Valor unitario: {precio_unitario}")
        valor_total = (precio_unitario * cantidad) - descuento
        st.write(f"Valor total: {valor_total}")
        submitted = st.form_submit_button("Registrar venta")
        if submitted:
            registrar_venta(prod_dict[producto_sel].id, tipo_precio, cantidad, descuento)
            st.success("Venta registrada")

    ventas = obtener_ventas()
    ventas_df = pd.DataFrame([{
        "Fecha": v["fecha"],
        "Producto": v["producto_nombre"],
        "Tipo Precio": v["tipo_precio"],
        "Cantidad": v["cantidad"],
        "Valor Unitario": v["valor_unitario"],
        "Valor Total": v["valor_total"],
        "Descuento": v["descuento"]
    } for v in ventas])
    st.dataframe(ventas_df)
    ventas_excel_buffer = io.BytesIO()
    ventas_df.to_excel(ventas_excel_buffer, index=False, engine='openpyxl')
    ventas_excel_buffer.seek(0)
    st.download_button(
        label="Descargar Ventas en Excel",
        data=ventas_excel_buffer,
        file_name="ventas.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="download_ventas"
    )

with tabs[2]:
    st.header("Stock actual (stock inicial - vendidos)")
    stock_actual_dict = obtener_stock_actual()
    stock_actual_df = pd.DataFrame([
        {
            "ID": pid,
            "Nombre": data["nombre"],
            "Stock Inicial": data["stock_inicial"],
            "Vendidos": data["vendidos"],
            "Stock Actual": data["stock_actual"]
        }
        for pid, data in stock_actual_dict.items()
    ])
    st.dataframe(stock_actual_df)
    stock_actual_excel_buffer = io.BytesIO()
    stock_actual_df.to_excel(stock_actual_excel_buffer, index=False, engine='openpyxl')
    stock_actual_excel_buffer.seek(0)
    st.download_button(
        label="Descargar Stock Actual en Excel",
        data=stock_actual_excel_buffer,
        file_name="stock_actual.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="download_stock_actual"
    )


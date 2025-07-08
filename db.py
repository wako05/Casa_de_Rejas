import os
import sys
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import datetime

# Obtiene el directorio base para los recursos.
# Si se ejecuta como un ejecutable de PyInstaller, sys._MEIPASS apunta
# al directorio temporal donde se extraen los archivos.
# De lo contrario, es el directorio del script actual.
if getattr(sys, 'frozen', False):
    # Ejecutando en un paquete de PyInstaller
    base_path = sys._MEIPASS
else:
    # Ejecutando en un entorno Python normal
    base_path = os.path.dirname(os.path.abspath(__file__))

# Construye la ruta completa al archivo de la base de datos.
# Asume que 'casa_rejas.db' está en el mismo directorio que db.py
# y que será copiado a la raíz del paquete de PyInstaller.
DATABASE_FILE = os.path.join(base_path, "casa_rejas.db")

# URL de la base de datos para SQLAlchemy
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# Crea el motor de la base de datos
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Crea una sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos declarativos
Base = declarative_base()

# Definición de los modelos de la base de datos
class Inventario(Base):
    __tablename__ = "inventario"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    caja_caliente = Column(Float, default=0)
    caja_fria = Column(Float, default=0)
    particular = Column(Float, default=0)
    six_pack = Column(Float, default=0)
    unitario = Column(Float, default=0)
    precio_compra = Column(Float, default=0)
    stock = Column(Integer, default=0)
    stock_minimo = Column(Integer, default=0)

class Venta(Base):
    __tablename__ = "ventas"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, default=datetime.date.today)
    producto_id = Column(Integer, ForeignKey('inventario.id'))
    tipo_precio = Column(String)
    cantidad = Column(Integer)
    valor_unitario = Column(Float)
    valor_total = Column(Float)
    descuento = Column(Integer, default=0)
    producto = relationship("Inventario")

# Función de utilidad para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para inicializar la base de datos (crear tablas)
def init_db():
    Base.metadata.create_all(bind=engine)

# Puedes llamar a init_db() aquí si quieres que se cree la base de datos
# automáticamente la primera vez que se ejecute el script, o llamarla
# desde main.py o ui.py.
init_db() # Descomenta si quieres que se cree la DB al importar db.py
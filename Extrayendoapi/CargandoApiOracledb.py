from config import *
import oracledb as ora
from Api import extract_and_transform

# Extracción y transformación
dim_exporter, dim_importer, dim_product, dim_unit, dim_year, main_table = extract_and_transform()

# Conexión
connection = ora.connect(user=USER, password=PASSWORD, dsn=DSN)
cursor = connection.cursor()

# Borrar tablas si existen
for table in ["MAIN_TABLE","DIM_EXPORTER","DIM_IMPORTER","DIM_PRODUCT","DIM_UNIT","DIM_YEAR"]:
    try:
        cursor.execute(f"DROP TABLE {table} PURGE")
    except ora.DatabaseError:
        print(f"⚠️ {table} no existía, se crea por primera vez.")

# Crear tablas e insertar datos
cursor.execute("""
CREATE TABLE DIM_EXPORTER (
    Exporter_ID VARCHAR2(20) PRIMARY KEY,
    Exporter_Country VARCHAR2(100)
)
""")
cursor.executemany(
    "INSERT INTO DIM_EXPORTER (Exporter_ID, Exporter_Country) VALUES (:1, :2)",
    dim_exporter.values.tolist()
)
connection.commit()

cursor.execute("""
CREATE TABLE DIM_IMPORTER (
    Importer_ID VARCHAR2(20) PRIMARY KEY,
    Importer_Country VARCHAR2(100)
)
""")
cursor.executemany(
    "INSERT INTO DIM_IMPORTER (Importer_ID, Importer_Country) VALUES (:1, :2)",
    dim_importer.values.tolist()
)
connection.commit()

cursor.execute("""
CREATE TABLE DIM_PRODUCT (
    Product_ID NUMBER PRIMARY KEY,
    HS6 VARCHAR2(255)
)
""")
cursor.executemany(
    "INSERT INTO DIM_PRODUCT (Product_ID,HS6) VALUES (:1, :2)",
    dim_product.values.tolist()
)
connection.commit()

cursor.execute("""
CREATE TABLE DIM_YEAR (
    Year_ID NUMBER PRIMARY KEY,
    Year NUMBER(4)
)
""")
cursor.executemany(
    "INSERT INTO DIM_YEAR (Year_ID, Year) VALUES (:1, :2)",
    dim_year.values.tolist()
)
connection.commit()

cursor.execute("""
CREATE TABLE DIM_UNIT (
    Unit_ID NUMBER PRIMARY KEY,
    Unit_Name VARCHAR2(100)
)
""")
cursor.executemany(
    "INSERT INTO DIM_UNIT (Unit_ID, Unit_Name) VALUES (:1, :2)",
    dim_unit.values.tolist()
)
connection.commit()

cursor.execute("""
CREATE TABLE MAIN_TABLE (
    Year_ID NUMBER,
    Exporter_ID VARCHAR2(20),
    Importer_ID VARCHAR2(20),
    Product_ID NUMBER,
    Unit_ID NUMBER,
    Trade_Value NUMBER,
    Quantity NUMBER,
    Unit_Value NUMBER,
    CONSTRAINT FK_MAIN_YEAR FOREIGN KEY (Year_ID) REFERENCES DIM_YEAR(Year_ID),
    CONSTRAINT FK_MAIN_EXPORTER FOREIGN KEY (Exporter_ID) REFERENCES DIM_EXPORTER(Exporter_ID),
    CONSTRAINT FK_MAIN_IMPORTER FOREIGN KEY (Importer_ID) REFERENCES DIM_IMPORTER(Importer_ID),
    CONSTRAINT FK_MAIN_PRODUCT FOREIGN KEY (Product_ID) REFERENCES DIM_PRODUCT(Product_ID),
    CONSTRAINT FK_MAIN_UNIT FOREIGN KEY (Unit_ID) REFERENCES DIM_UNIT(Unit_ID)
)
""")
cursor.executemany(
    """INSERT INTO MAIN_TABLE
    (Year_ID,Exporter_ID,Importer_ID,Product_ID,Unit_ID,Trade_Value,Quantity,Unit_Value)
    VALUES (:1, :2, :3, :4, :5, :6, :7, :8)""",
    main_table.values.tolist()
)
connection.commit()

cursor.close()
connection.close()
print("✅ Tablas creadas e insertadas correctamente.")



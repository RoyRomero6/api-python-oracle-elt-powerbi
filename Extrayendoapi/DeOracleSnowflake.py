import oracledb as ora
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from config import *


# ===============================
# 🔌 CONEXIONES
# ===============================

# Oracle
ORA_USER = USER
ORA_PASS = PASSWORD
ORA_DSN = DSN

# Snowflake
SF_USER = SF_USER
SF_PASS = SF_PASS
SF_ACCOUNT = SF_ACCOUNT
SF_WAREHOUSE = SF_WAREHOUSE
SF_DATABASE = SF_DATABASE
SF_SCHEMA = SF_SCHEMA


# ===============================
# 📥 EXTRACCIÓN DESDE ORACLE
# ===============================
def extract_from_oracle():
    print("Conectando a Oracle...")

    conn = ora.connect(user=ORA_USER, password=ORA_PASS, dsn=ORA_DSN)

    tables = [
        "DIM_EXPORTER",
        "DIM_IMPORTER",
        "DIM_PRODUCT",
        "DIM_UNIT",
        "DIM_YEAR",
        "MAIN_TABLE"
    ]

    dataframes = {}

    for table in tables:
        print(f"📤 Extrayendo datos de {table}...")
        df = pd.read_sql(f"SELECT * FROM {table}", conn)
        print(f"   → {len(df)} filas obtenidas.")
        dataframes[table] = df

    conn.close()
    return dataframes


# ===============================
# 📤 CARGA A SNOWFLAKE
# ===============================
def load_to_snowflake(dataframes):
    print("🔹 Conectando a Snowflake...")

    conn_sf = snowflake.connector.connect(
        user=SF_USER,
        password=SF_PASS,
        account=SF_ACCOUNT,
        warehouse=SF_WAREHOUSE,
        database=SF_DATABASE,
        schema=SF_SCHEMA
    )

    for table, df in dataframes.items():
        print(f"🚀 Cargando {table} a Snowflake...")

        success, nchunks, nrows, _ = write_pandas(
            conn_sf,
            df,
            table_name=table,
            auto_create_table=True,
            overwrite=True
        )

        print(f"   ✔ {table}: {nrows} filas insertadas.")

    conn_sf.close()


# ===============================
# 🧩 FLOW COMPLETO
# ===============================
def oracle_to_snowflake_flow():

    try:
        dfs = extract_from_oracle()
        load_to_snowflake(dfs)

        msg = "El flujo Oracle→Snowflake finalizó correctamente."
        print(msg)

    except Exception as e:
        msg = f"El flujo falló con el error:\n{e}"
        print(msg)

# Ejecutar
if __name__ == "__main__":
    oracle_to_snowflake_flow()

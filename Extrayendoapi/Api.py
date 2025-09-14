#!/usr/bin/env python
# coding: utf-8

# In[13]:
import requests
import pandas as pd

def extract_and_transform():
    url = "https://api-v2.oec.world/tesseract/data.jsonrecords"
    params = {
        "cube": "trade_i_baci_a_22",
        "drilldowns": "Year,Exporter Country,Importer Country,HS6,Unit",
        "measures": "Trade Value,Quantity,Unit Value",
        "limit": "10000,0"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(f"❌ Error {response.status_code}: {response.text}")

    data = response.json().get("data", [])
    df = pd.DataFrame(data)

    # --- Creación de dimensiones ---
    dim_exporter = df[['Exporter Country ID', 'Exporter Country']].drop_duplicates().rename(
        columns={'Exporter Country ID': 'Exporter_ID', 'Exporter Country': 'Exporter_Country'})

    dim_importer = df[['Importer Country ID', 'Importer Country']].drop_duplicates().rename(
        columns={'Importer Country ID': 'Importer_ID', 'Importer Country': 'Importer_Country'})

    dim_product = df[['HS6 ID', 'HS6']].drop_duplicates().rename(
        columns={'HS6 ID': 'Product_ID'})

    dim_unit = df[['Unit ID', 'Unit']].drop_duplicates().rename(
        columns={'Unit ID': 'Unit_ID', 'Unit': 'Unit_Name'})

    dim_year = df[['Year']].drop_duplicates().reset_index(drop=True)
    dim_year['Year_ID'] = dim_year.index + 1
    dim_year = dim_year[['Year_ID', 'Year']]

    # Merge para crear la tabla de hechos
    df = df.merge(dim_year, on='Year', how='left')
    main_table = df[['Year_ID', 'Exporter Country ID', 'Importer Country ID',
                    'HS6 ID', 'Unit ID', 'Trade Value', 'Quantity', 'Unit Value']].rename(
        columns={
            'Exporter Country ID': 'Exporter_ID',
            'Importer Country ID': 'Importer_ID',
            'HS6 ID': 'Product_ID',
            'Unit ID': 'Unit_ID',
            'Trade Value': 'Trade_Value',
            'Unit Value': 'Unit_Value'
        }
    )
    import numpy as np
    main_table = main_table.replace({np.nan: None})
    return dim_exporter, dim_importer, dim_product, dim_unit, dim_year, main_table


if __name__ == "__main__":
    dims = extract_and_transform()
    for i, df in enumerate(dims):
        print(f"Tabla {i+1}: {df.shape[0]} filas")
show warehouses;
use warehouse SYSTEM$STREAMLIT_NOTEBOOK_WH;
create or replace database sf_db;
use database sf_db;
create schema trade_sf;
use schema trade_sf;
--Comprobación de tablas
select * from DIM_EXPORTER;
select * from DIM_IMPORTER;
select * from DIM_PRODUCT;
select * from DIM_UNIT;
select * from DIM_YEAR;
select * from MAIN_TABLE;
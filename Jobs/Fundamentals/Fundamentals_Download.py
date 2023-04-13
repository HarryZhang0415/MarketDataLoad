from Utils.DataProvider.FMP import FMP
from Utils.SQLAlchemy.Fundamentals_Staging import *
from Utils.SQLAlchemy import format_dataframe
from sqlalchemy import create_engine, URL
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
import logging
import sys

load_dotenv()

def Download_Company_Info(engine, data_vendor, datatype):
    table = CompanyInfo_Staging()

    logging.info("Get constituents company list from DJ/SP/NQ")
    sp500_cons_df = data_vendor.Sp500_Constituents(datatype)
    nasdaq_100_df = data_vendor.Nasdaq_100(datatype)
    dj_cons_df = data_vendor.DJ_Constituents(datatype)
    universe = pd.concat([sp500_cons_df, nasdaq_100_df, dj_cons_df], axis=0).drop_duplicates(subset=table.primary_key).set_index(table.primary_key)

    logging.info("Universe Downloaded")

    core_info = []
    for symbol in universe.symbol:
        core_info_tmp = data_vendor.Company_Core_Information(symbol, datatype=datatype, url_only=True)
        core_info.append(core_info_tmp)

    logging.info("Start Downloading Company Core Info")
    results = data_vendor.multi_thread_endpoint_wrapper(core_info)
    logging.info("Finished")
    core_info_df = pd.DataFrame()
    for r in results:
        tmp_df = pd.DataFrame(r)
        core_info_df = pd.concat([core_info_df, tmp_df])

    core_info_df = core_info_df.drop_duplicates(subset=table.primary_key).set_index(table.primary_key)

    cols_to_use = core_info_df.columns.difference(universe.columns)
    Company_Info = pd.merge(universe, core_info_df[cols_to_use], left_index=True, right_index=True)

    columns = [col for col in table.fmp_column_mapping.values() if col in Company_Info.columns]

    Company_Info = Company_Info[columns].replace(r'^\s*$', np.nan, regex=True)
    dtype_map = {col.name: col.type for col in table.__table__.columns}

    df_agg = format_dataframe(Company_Info, dtype_map, format_index=True)
    logging.info("Start Inserting Data Into Database")
    df_agg[columns].to_sql(name=table.__tablename__, con=engine, if_exists='replace', index=True)

    logging.info("Finished")

    return df_agg['symbol']


def Download_Income_Statement(engine, data_vendor, symbol_list, period, datatype, limit):

    table = IncomeStatement_Staging()

    logging.info("Start Constructing API Call Urls")
    url_list = []

    for symbol in symbol_list:
        url = data_vendor.Income_Statement(symbol, datatype=datatype, period = period, limit = limit, url_only=True)
        url_list.append(url)

    results = data_vendor.multi_thread_endpoint_wrapper(url_list)

    logging.info("Start Parsing Results")
    df_agg = pd.DataFrame()
    for r in results:
        tmp_df = pd.DataFrame(r)
        df_agg = pd.concat([df_agg, tmp_df])

    columns = [col for col in table.fmp_column_mapping.values() if col in df_agg.columns]
    df_agg = df_agg[columns].dropna(subset=table.primary_key).drop_duplicates(subset=table.primary_key)

    dtype_map = {col.name: col.type for col in table.__table__.columns}

    df_agg = format_dataframe(df_agg, dtype_map)   

    logging.info("Insert Into Database - Table Name %s" % table.__tablename__)
    # Write the DataFrame to the SQL table, mapping the columns
    df_agg[columns].to_sql(name=table.__tablename__, con=engine, if_exists='replace', index=False)


def Download_Balance_Sheet(engine, data_vendor, symbol, period, datatype, limit):
    table = BalanceSheet_Staging()

    logging.info("Start Constructing API Call Urls")
    url_list = []

    for symbol in symbol_list:
        url = data_vendor.Balance_Sheet_Statement(symbol, datatype=datatype, period = period, limit = limit, url_only=True)
        url_list.append(url)

    results = data_vendor.multi_thread_endpoint_wrapper(url_list)
    
    logging.info("Start Parsing Results")
    df_agg = pd.DataFrame()
    for r in results:
        tmp_df = pd.DataFrame(r)
        df_agg = pd.concat([df_agg, tmp_df])

    columns = [col for col in table.fmp_column_mapping.values() if col in df_agg.columns]
    df_agg = df_agg[columns].dropna(subset=table.primary_key).drop_duplicates(subset=table.primary_key)

    dtype_map = {col.name: col.type for col in table.__table__.columns}

    df_agg = format_dataframe(df_agg, dtype_map)

    logging.info("Insert Into Database - Table Name %s" % table.__tablename__)
    # Write the DataFrame to the SQL table, mapping the columns
    df_agg[columns].to_sql(name=table.__tablename__, con=engine, if_exists='replace', index=False)


def Download_Cashflow_Statement(engine, data_vendor, symbol, period, datatype, limit):
    table = CashflowStatement_Staging()

    logging.info("Start Constructing API Call Urls")
    url_list = []

    for symbol in symbol_list:
        url = data_vendor.Cash_Flow_Statement(symbol, datatype=datatype, period = period, limit = limit, url_only=True)
        url_list.append(url)

    results = data_vendor.multi_thread_endpoint_wrapper(url_list)
    
    logging.info("Start Parsing Results")
    df_agg = pd.DataFrame()
    for r in results:
        tmp_df = pd.DataFrame(r)
        df_agg = pd.concat([df_agg, tmp_df])

    columns = [col for col in table.fmp_column_mapping.values() if col in df_agg.columns]
    df_agg = df_agg.dropna(subset=table.primary_key).drop_duplicates(subset=table.primary_key)

    dtype_map = {col.name: col.type for col in table.__table__.columns}

    df_agg = format_dataframe(df_agg, dtype_map)

    logging.info("Insert Into Database - Table Name %s" % table.__tablename__)
    # Write the DataFrame to the SQL table, mapping the columns
    df_agg[columns].to_sql(name=table.__tablename__, con=engine, if_exists='replace', index=False)

if __name__ == '__main__':

    log_path = os.getenv('log_location') + 'Fundamental_Download.log'
    log_format = '%(asctime)s - %(module)s - %(funcName)20s() - %(levelname)s - %(message)s'
    logging.basicConfig(filename=log_path, level=logging.INFO, format=log_format)
    
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter(log_format)
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)

    connector = os.getenv('database_connector')
    username = os.getenv('database_username')
    password = os.getenv('database_password')
    host = os.getenv('database_host')
    datatype = 'csv' ## return pandas dataframe
    period = 'quarter' # 'quarter' 'annual'
    limit = 120
    database = 'fundamentals_staging'

    url_object = URL.create(
        connector,
        username=username,
        password=password,
        host=host,
        database=database,
    )

    engine = create_engine(url_object)
    logging.info("Create Database Engine")
    
    data_vendor = FMP()
    logging.info("Initialize Data Vendor Class")

    logging.info("Start Download Company Info")
    symbol_list = Download_Company_Info(engine, data_vendor, datatype)

    Download_Income_Statement(engine, data_vendor, symbol_list, period, datatype, limit)
    Download_Balance_Sheet(engine, data_vendor, symbol_list, period, datatype, limit)
    Download_Cashflow_Statement(engine, data_vendor, symbol_list, period, datatype, limit)
    

from Utils.DataProvider.FMP import FMP
from Utils.SQLAlchemy.Fundamentals import *
from Utils.LoggingService import LoggingService
from sqlalchemy import create_engine, URL
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()
log_path = os.getenv('log_location') + 'Fundamental_Download.log'
logger = LoggingService('Fundamental_Download', log_file=log_path)

def Download_Company_Info(engine, data_vendor, datatype):
    logger.info("Get constituents company list from DJ/SP/NQ")
    sp500_cons_df = data_vendor.Sp500_Constituents(datatype)
    nasdaq_100_df = data_vendor.Nasdaq_100(datatype)
    dj_cons_df = data_vendor.DJ_Constituents(datatype)
    universe = pd.concat([sp500_cons_df, nasdaq_100_df, dj_cons_df], axis=0).drop_duplicates(subset=['cik']).set_index('cik')

    logger.info("Universe Downloaded")

    core_info = []
    for symbol in universe.symbol:
        core_info_tmp = data_vendor.Company_Core_Information(symbol, datatype=datatype, url_only=True)
        core_info.append(core_info_tmp)

    logger.info("Start Downloading Company Core Info")
    results = data_vendor.multi_thread_endpoint_wrapper(core_info)
    logger.info("Finished")
    core_info_df = pd.DataFrame()
    for r in results:
        tmp_df = pd.DataFrame(r)
        core_info_df = pd.concat([core_info_df, tmp_df])

    core_info_df = core_info_df.drop_duplicates(subset=['cik']).set_index('cik')

    cols_to_use = core_info_df.columns.difference(universe.columns)
    Company_Info = pd.merge(universe, core_info_df[cols_to_use], left_index=True, right_index=True)

    # Define the DataFrame and the table name
    table_name = CompanyInfo.__tablename__

    columns = [col for col in fmp_column_mapping_companyinfo.values() if col in Company_Info.columns]

    Company_Info = Company_Info[columns].replace(r'^\s*$', np.nan, regex=True)
    logger.info("Start Inserting Data Into Database")
    # Company_Info.to_sql(name=table_name, con=engine, if_exists='append', index=True)
    logger.info("Finished")


def Download_Income_Statement(engine, data_vendor, symbol, period, datatype, limit):

    Income_Statement = data_vendor.Income_Statement(symbol, period=period, datatype=datatype, limit=limit)

    columns = [col for col in fmp_column_mapping_incomestatement.values() if col in Income_Statement.columns]

    # Define the DataFrame and the table name
    table_name = IncomeStatement.__tablename__

    # Write the DataFrame to the SQL table, mapping the columns
    Income_Statement[columns].to_sql(name=table_name, con=engine, if_exists='append', index=True)


def Download_Balance_Sheet(engine, data_vendor, symbol, period, datatype, limit):

    Balance_Sheet_Statement = data_vendor.Balance_Sheet_Statement(symbol, period=period, datatype=datatype, limit=limit)

    columns = [col for col in fmp_column_mapping_balancesheet.values() if col in Balance_Sheet_Statement.columns]

    # Define the DataFrame and the table name
    table_name = BalanceSheet.__tablename__

    # Write the DataFrame to the SQL table, mapping the columns
    Balance_Sheet_Statement[columns].to_sql(name=table_name, con=engine, if_exists='append', index=True)

def Download_Cashflow_Statement(engine, data_vendor, symbol, period, datatype, limit):

    Cash_Flow_Statement = data_vendor.Cash_Flow_Statement(symbol, period=period, datatype=datatype, limit=limit)

    columns = [col for col in fmp_column_mapping_cashflowstatement.values() if col in Cash_Flow_Statement.columns]

    # Define the DataFrame and the table name
    table_name = CashflowStatement.__tablename__

    # Write the DataFrame to the SQL table, mapping the columns
    Cash_Flow_Statement[columns].to_sql(name=table_name, con=engine, if_exists='append', index=True)


if __name__ == '__main__':

    # Create a SQLAlchemy engine
    symbol = 'AAPL'
    period = 'quarter' # 'quarter' 'annual'
    datatype = 'csv' ## return pandas dataframe
    limit = 120

    connector = os.getenv('database_connector')
    username = os.getenv('database_username')
    password = os.getenv('database_password')
    host = os.getenv('database_host')

    database = 'fundamentals'

    url_object = URL.create(
        connector,
        username=username,
        password=password,
        host=host,
        database=database,
    )

    engine = create_engine(url_object)
    logger.info("Create Database Engine")
    
    data_vendor = FMP()

    import logging

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    data_vendor.logger.logger.addHandler(file_handler)

    logger.info("Initialize Data Vendor Class")

    logger.info("Start Download Company Info")
    Download_Company_Info(engine, data_vendor, datatype)
    # Download_Income_Statement(engine, data_vendor, symbol, period, datatype, limit)
    # Download_Balance_Sheet(engine, data_vendor, symbol, period, datatype, limit)
    # Download_Cashflow_Statement(engine, data_vendor, symbol, period, datatype, limit)
    

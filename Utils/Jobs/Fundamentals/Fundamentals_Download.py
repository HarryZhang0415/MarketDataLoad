from Utils.DataProvider.FMP import FMP
from Utils.SQLAlchemy.Fundamentals import *
from sqlalchemy import create_engine
from fundamentals_config import *


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

    url_object = URL.create(
        connector,
        username=username,
        password=password,
        host=host,
        database=database,
    )

    engine = create_engine(url_object)
    data_vendor = FMP()

    # Download_Income_Statement(engine, data_vendor, symbol, period, datatype, limit)
    # Download_Balance_Sheet(engine, data_vendor, symbol, period, datatype, limit)
    Download_Cashflow_Statement(engine, data_vendor, symbol, period, datatype, limit)


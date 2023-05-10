from dotenv import load_dotenv
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import os
import logging

load_dotenv()

if __name__ == '__main__':

    log_path = os.getenv('log_location') + 'Syncing_Data.log'
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

    database = 'fundamentals_staging'

    url_object = URL.create(
        connector,
        username=username,
        password=password,
        host=host,
        database=database,
    )

    engine = create_engine(url_object)

    Session = sessionmaker(engine)

    with Session() as session:
        session.execute(text("CALL syncing_company_info();"))
        logging.info("Finished syncing company info table")

        session.execute(text("CALL syncing_income_statement();"))
        logging.info("Finished syncing income statement table")

        session.execute(text("CALL syncing_balance_sheet();"))
        logging.info("Finished syncing balance sheet table")

        session.execute(text("CALL syncing_cashflow_statement();"))
        logging.info("Finished syncing cashflow statement table")

        session.commit()
    
    logging.info("Syncing Finished.")


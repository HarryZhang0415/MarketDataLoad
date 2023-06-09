from sqlalchemy import Column, Integer, String, create_engine, URL, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

load_dotenv()

# Columns of the table in database : Columns of the dataframe generated from FMP.
Base = declarative_base()

class CompanyInfo(Base):
    __tablename__ = 'company_info'

    ID = Column(Integer, autoincrement=True)
    cik = Column(Integer, primary_key=True, nullable=False)
    symbol = Column(String(20))
    name = Column(String(200))
    sicDescription = Column(String)
    sicGroup = Column(String(200))
    sicCode = Column(Integer)
    sector = Column(String(20))
    subSector = Column(String(200))
    exchange = Column(String(20))
    headQuarter = Column(String(20))
    stateLocation = Column(String(20))
    stateOfIncorporation = Column(String(20))
    fiscalYearEnd = Column(String(5))
    businessAddress = Column(String(200))
    mailingAddress = Column(String(200))
    taxIdentificationNumber = Column(String(20))
    registrantName = Column(String(200))

    fmp_column_mapping = {
    'cik': 'cik',
    'symbol': 'symbol',
    'name': 'name',
    'sicDescription': 'sicDescription',
    'sicGroup': 'sicGroup',
    'sicCode': 'sicCode',
    'sector': 'sector',
    'subSector': 'subSector',
    'exchange': 'exchange',
    'headQuarter': 'headQuarter',
    'stateLocation': 'stateLocation',
    'stateOfIncorporation': 'stateOfIncorporation',
    'fiscalYearEnd': 'fiscalYearEnd',
    'businessAddress': 'businessAddress',
    'mailingAddress': 'mailingAddress',
    'taxIdentificationNumber': 'taxIdentificationNumber',
    'registrantName': 'registrantName'
    }

    @property
    def primary_key(self):
        return [key.name for key in inspect(__class__).primary_key]
    
    def get_all_record_from_db(self):
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

        with Session(engine) as session:
            statement = select(__class__)
            records = session.execute(statement).all()

        return records

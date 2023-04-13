from sqlalchemy import Column, Integer, String, create_engine, URL, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

load_dotenv()

# Columns of the table in database : Columns of the dataframe generated from FMP.
Base = declarative_base()

class CompanyInfo_Staging(Base):
    __tablename__ = 'company_info'

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
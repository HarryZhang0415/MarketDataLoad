from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Columns of the table in database : Columns of the dataframe generated from FMP.
fmp_column_mapping_companyinfo = {
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

Base = declarative_base()

class CompanyInfo(Base):
    __tablename__ = 'company_info'

    ID = Column(Integer, primary_key=True)
    cik = Column(Integer, nullable=False)
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
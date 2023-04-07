from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

# Columns of the table in database : Columns of the dataframe generated from FMP.
fmp_column_mapping_universe = {
    "cik": "cik",
    "symbol": "symbol",
    "name": "name",
    "sector": "sector",
    "subSector": "subSector",
    "headQuarter": "headQuarter"
}

Base = declarative_base()

class Universe(Base):
    __tablename__ = 'universe'

    cik = Column(Integer, primary_key=True)
    symbol = Column(String(20))
    name = Column(String(200))
    sector = Column(String(200))
    subSector = Column(String(200))
    headQuarter = Column(String(200))

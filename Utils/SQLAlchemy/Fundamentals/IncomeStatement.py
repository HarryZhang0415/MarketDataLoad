from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base

# engine = create_engine('mysql://username:password@host/database_name')

fmp_column_mapping_incomestatement = {
# Columns of the table in database : Columns of the dataframe generated from FMP.
  'cik': 'cik',
  'calendarYear': 'calendarYear',
  'period' : 'period',
  'revenue' : 'revenue',
  'costOfRevenue' : 'costOfRevenue' ,
  'grossProfit' : 'grossProfit' ,
  'researchAndDevelopmentExpenses' : 'researchAndDevelopmentExpenses',
  'generalAndAdministrativeExpenses' : 'generalAndAdministrativeExpenses' ,
  'sellingAndMarketingExpenses' : 'sellingAndMarketingExpenses' ,
  'sellingGeneralAndAdministrativeExpenses' : 'sellingGeneralAndAdministrativeExpenses' ,
  'otherExpenses' : 'otherExpenses' ,
  'operatingExpenses' : 'operatingExpenses' ,
  'costAndExpenses' : 'costAndExpenses', 
  'interestIncome' : 'interestIncome',
  'interestExpense' : 'interestExpense',
  'depreciationAndAmortization' : 'depreciationAndAmortization',
  'ebitda' : 'ebitda',
  'operatingIncome' : 'operatingIncome',
  'totalOtherIncomeExpensesNet' : 'totalOtherIncomeExpensesNet',
  'incomeBeforeTax' : 'incomeBeforeTax',
  'incomeTaxExpense' : 'incomeTaxExpense',
  'netIncome' : 'netIncome'
}

Base = declarative_base()

class IncomeStatement(Base):
    __tablename__ = 'income_statement'
    
    ID = Column(Integer, primary_key=True, autoincrement=True)
    cik = Column(Integer, primary_key=True, nullable=False)
    calendarYear = Column(String(5), primary_key=True, nullable=False)
    period = Column(String(5), primary_key=True, nullable=False)
    revenue = Column(Numeric(20, 4))
    costOfRevenue = Column(Numeric(20, 4))
    grossProfit = Column(Numeric(20, 4))
    researchAndDevelopmentExpenses = Column(Numeric(20, 4))
    generalAndAdministrativeExpenses = Column(Numeric(20, 4))
    sellingAndMarketingExpenses = Column(Numeric(20, 4))
    sellingGeneralAndAdministrativeExpenses = Column(Numeric(20, 4))
    otherExpenses = Column(Numeric(20, 4))
    operatingExpenses = Column(Numeric(20, 4))
    costAndExpenses = Column(Numeric(20, 4))
    interestIncome = Column(Numeric(20, 4))
    interestExpense = Column(Numeric(20, 4))
    depreciationAndAmortization = Column(Numeric(20, 4))
    ebitda = Column(Numeric(20, 4))
    operatingIncome = Column(Numeric(20, 4))
    totalOtherIncomeExpensesNet = Column(Numeric(20, 4))
    incomeBeforeTax = Column(Numeric(20, 4))     
    incomeTaxExpense = Column(Numeric(20, 4))
    netIncome = Column(Numeric(20, 4))
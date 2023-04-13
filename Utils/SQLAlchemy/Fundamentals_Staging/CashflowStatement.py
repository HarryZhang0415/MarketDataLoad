

from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.inspection import inspect

Base = declarative_base()

class CashflowStatement_Staging(Base):
    __tablename__ = 'cashflow_statement'

    cik = Column(Integer, nullable=False, primary_key=True)
    calendarYear = Column(String(5), nullable=False, primary_key=True)
    period = Column(String(5), nullable=False, primary_key=True)
    netIncome = Column(DECIMAL(20,4))
    depreciationAndAmortization = Column(DECIMAL(20,4))
    deferredIncomeTax = Column(DECIMAL(20,4))
    stockBasedCompensation = Column(DECIMAL(20,4))
    changeInWorkingCapital = Column(DECIMAL(20,4))
    accountsReceivables = Column(DECIMAL(20,4))
    inventory = Column(DECIMAL(20,4))
    accountsPayables = Column(DECIMAL(20,4))
    otherWorkingCapital = Column(DECIMAL(20,4))
    otherNonCashItems = Column(DECIMAL(20,4))
    netCashProvidedByOperatingActivities = Column(DECIMAL(20,4))
    investmentsInPropertyPlantAndEquipment = Column(DECIMAL(20,4))
    acquisitionsNet = Column(DECIMAL(20,4))
    purchasesOfInvestments = Column(DECIMAL(20,4))
    salesMaturitiesOfInvestments = Column(DECIMAL(20,4))
    otherInvestingActivites = Column(DECIMAL(20,4))
    netCashUsedForInvestingActivites = Column(DECIMAL(20,4))
    debtRepayment = Column(DECIMAL(20,4))
    commonStockIssued = Column(DECIMAL(20,4))
    commonStockRepurchased = Column(DECIMAL(20,4))
    dividendsPaid = Column(DECIMAL(20,4))
    otherFinancingActivites = Column(DECIMAL(20,4))
    netCashUsedProvidedByFinancingActivities = Column(DECIMAL(20,4))
    effectOfForexChangesOnCash = Column(DECIMAL(20,4))
    netChangeInCash = Column(DECIMAL(20,4))
    cashAtEndOfPeriod = Column(DECIMAL(20,4))
    cashAtBeginningOfPeriod = Column(DECIMAL(20,4))
    operatingCashFlow = Column(DECIMAL(20,4))
    capitalExpenditure = Column(DECIMAL(20,4))
    freeCashFlow = Column(DECIMAL(20,4))

    # Columns of the table in database : Columns of the dataframe generated from FMP.
    fmp_column_mapping = {
        'cik': 'cik',
        'calendarYear': 'calendarYear',
        'period': 'period',
        'netIncome': 'netIncome',
        'depreciationAndAmortization': 'depreciationAndAmortization',
        'deferredIncomeTax': 'deferredIncomeTax',
        'stockBasedCompensation': 'stockBasedCompensation',
        'changeInWorkingCapital': 'changeInWorkingCapital',
        'accountsReceivables': 'accountsReceivables',
        'inventory': 'inventory',
        'accountsPayables': 'accountsPayables',
        'otherWorkingCapital': 'otherWorkingCapital',
        'otherNonCashItems': 'otherNonCashItems',
        'netCashProvidedByOperatingActivities': 'netCashProvidedByOperatingActivities',
        'investmentsInPropertyPlantAndEquipment': 'investmentsInPropertyPlantAndEquipment',
        'acquisitionsNet': 'acquisitionsNet',
        'purchasesOfInvestments': 'purchasesOfInvestments',
        'salesMaturitiesOfInvestments': 'salesMaturitiesOfInvestments',
        'otherInvestingActivites': 'otherInvestingActivites',
        'netCashUsedForInvestingActivites': 'netCashUsedForInvestingActivites',
        'debtRepayment': 'debtRepayment',
        'commonStockIssued': 'commonStockIssued',
        'commonStockRepurchased': 'commonStockRepurchased',
        'dividendsPaid': 'dividendsPaid',
        'otherFinancingActivites': 'otherFinancingActivites',
        'netCashUsedProvidedByFinancingActivities': 'netCashUsedProvidedByFinancingActivities',
        'effectOfForexChangesOnCash': 'effectOfForexChangesOnCash',
        'netChangeInCash': 'netChangeInCash',
        'cashAtEndOfPeriod': 'cashAtEndOfPeriod',
        'cashAtBeginningOfPeriod': 'cashAtBeginningOfPeriod',
        'operatingCashFlow': 'operatingCashFlow',
        'capitalExpenditure': 'capitalExpenditure',
        'freeCashFlow': 'freeCashFlow'
    }

    @property
    def primary_key(self):
        return [key.name for key in inspect(__class__).primary_key]
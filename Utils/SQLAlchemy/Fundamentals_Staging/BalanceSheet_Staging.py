from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.inspection import inspect

Base = declarative_base()

class BalanceSheet_Staging(Base):
    __tablename__ = 'balancesheet_staging'
    
    cik = Column(Integer, nullable=False, primary_key=True)
    calendarYear = Column(String(5), nullable=False, primary_key=True)
    period = Column(String(5), nullable=False, primary_key=True)
    cashAndCashEquivalents = Column(Numeric(20, 4))
    shortTermInvestments = Column(Numeric(20, 4))
    cashAndShortTermInvestments = Column(Numeric(20, 4))
    netReceivables = Column(Numeric(20, 4))
    inventory = Column(Numeric(20, 4))
    otherCurrentAssets = Column(Numeric(20, 4))
    totalCurrentAssets = Column(Numeric(20, 4))
    propertyPlantEquipmentNet = Column(Numeric(20, 4))
    goodwill = Column(Numeric(20, 4))
    intangibleAssets = Column(Numeric(20, 4))
    goodwillAndIntangibleAssets = Column(Numeric(20, 4))
    longTermInvestments = Column(Numeric(20, 4))
    taxAssets = Column(Numeric(20, 4))
    otherNonCurrentAssets = Column(Numeric(20, 4))
    totalNonCurrentAssets = Column(Numeric(20, 4))
    otherAssets = Column(Numeric(20, 4))
    totalAssets = Column(Numeric(20, 4))
    accountPayables = Column(Numeric(20, 4))
    shortTermDebt = Column(Numeric(20, 4))
    taxPayables = Column(Numeric(20, 4))
    deferredRevenue = Column(Numeric(20, 4))
    otherCurrentLiabilities = Column(Numeric(20, 4))
    totalCurrentLiabilities = Column(Numeric(20, 4))
    longTermDebt = Column(Numeric(20, 4))
    deferredRevenueNonCurrent = Column(Numeric(20, 4))
    deferredTaxLiabilitiesNonCurrent = Column(Numeric(20, 4))
    otherNonCurrentLiabilities = Column(Numeric(20, 4))
    totalNonCurrentLiabilities = Column(Numeric(20, 4))
    otherLiabilities = Column(Numeric(20, 4))
    capitalLeaseObligations = Column(Numeric(20, 4))
    totalLiabilities = Column(Numeric(20, 4))
    preferredStock = Column(Numeric(20, 4))
    commonStock = Column(Numeric(20, 4))
    retainedEarnings = Column(Numeric(20, 4))
    accumulatedOtherComprehensiveIncomeLoss = Column(Numeric(20, 4))
    othertotalStockholdersEquity = Column(Numeric(20, 4))
    totalStockholdersEquity = Column(Numeric(20, 4))
    totalEquity = Column(Numeric(20, 4))
    totalLiabilitiesAndStockholdersEquity = Column(Numeric(20, 4))
    minorityInterest = Column(Numeric(20, 4))
    totalLiabilitiesAndTotalEquity = Column(Numeric(20, 4))
    totalInvestments = Column(Numeric(20, 4))
    totalDebt = Column(Numeric(20, 4))
    netDebt = Column(Numeric(20, 4))

    # Columns of the table in database : Columns of the dataframe generated from FMP.
    fmp_column_mapping = {
    'cik': 'cik',
    'calendarYear': 'calendarYear',
    'period': 'period',
    'cashAndCashEquivalents': 'cashAndCashEquivalents',
    'shortTermInvestments': 'shortTermInvestments',
    'cashAndShortTermInvestments': 'cashAndShortTermInvestments',
    'netReceivables': 'netReceivables',
    'inventory': 'inventory',
    'otherCurrentAssets': 'otherCurrentAssets',
    'totalCurrentAssets': 'totalCurrentAssets',
    'propertyPlantEquipmentNet': 'propertyPlantEquipmentNet',
    'goodwill': 'goodwill',
    'intangibleAssets': 'intangibleAssets',
    'goodwillAndIntangibleAssets': 'goodwillAndIntangibleAssets',
    'longTermInvestments': 'longTermInvestments',
    'taxAssets': 'taxAssets',
    'otherNonCurrentAssets': 'otherNonCurrentAssets',
    'totalNonCurrentAssets': 'totalNonCurrentAssets',
    'otherAssets': 'otherAssets',
    'totalAssets': 'totalAssets',
    'accountPayables': 'accountPayables',
    'shortTermDebt': 'shortTermDebt',
    'taxPayables': 'taxPayables',
    'deferredRevenue': 'deferredRevenue',
    'otherCurrentLiabilities': 'otherCurrentLiabilities',
    'totalCurrentLiabilities': 'totalCurrentLiabilities',
    'longTermDebt': 'longTermDebt',
    'deferredRevenueNonCurrent': 'deferredRevenueNonCurrent',
    'deferredTaxLiabilitiesNonCurrent': 'deferredTaxLiabilitiesNonCurrent',
    'otherNonCurrentLiabilities': 'otherNonCurrentLiabilities',
    'totalNonCurrentLiabilities': 'totalNonCurrentLiabilities',
    'otherLiabilities': 'otherLiabilities',
    'capitalLeaseObligations': 'capitalLeaseObligations',
    'totalLiabilities': 'totalLiabilities',
    'preferredStock': 'preferredStock',
    'commonStock': 'commonStock',
    'retainedEarnings': 'retainedEarnings',
    'accumulatedOtherComprehensiveIncomeLoss': 'accumulatedOtherComprehensiveIncomeLoss',
    'othertotalStockholdersEquity': 'othertotalStockholdersEquity',
    'totalStockholdersEquity': 'totalStockholdersEquity',
    'totalEquity': 'totalEquity',
    'totalLiabilitiesAndStockholdersEquity': 'totalLiabilitiesAndStockholdersEquity',
    'minorityInterest': 'minorityInterest',
    'totalLiabilitiesAndTotalEquity': 'totalLiabilitiesAndTotalEquity',
    'totalInvestments': 'totalInvestments',
    'totalDebt': 'totalDebt',
    'netDebt': 'netDebt'
    }   

    @property
    def primary_key(self):
        return [key.name for key in inspect(__class__).primary_key]
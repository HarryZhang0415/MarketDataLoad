from Utils.DataProvider import mysql_config, api_key_sql
import mysql.connector
import requests
import pandas as pd
import datetime
import time
import threading
from Utils.DataProvider.APICaller import *
import os
import logging

class FMP(object):

    def __init__(self) -> None:

        self.api_key = None

        self._max_try = 5
        self._api_call_limit_per_minute = 700
        self._api_call_ct = self._api_call_limit_per_minute
        self._worker_ct = 25
        self._sleep_time = 60 # seconds

        cnx = mysql.connector.connect(**mysql_config)
        cursor = cnx.cursor()
        cursor.execute(api_key_sql, [FMP.__name__, FMP.__name__])

        for _ in cursor:
            self.api_key = _[0]

        try: 
            url = 'https://site.financialmodelingprep.com/developer/docs'
            request = requests.get(url, timeout=5)
            logging.info('FMP Connection Established')
        except:
            logging.error("FMP Connection Failed")

    
    def multi_thread_endpoint_wrapper(self, function_list):
        logging.info("Initialize The APICaller Class For Multi Threading")
        Caller = APICaller(self._max_try, self._sleep_time, self._api_call_limit_per_minute)
        results = Caller.call_api_in_parallel(function_list)

        logging.info("Finished. Return Restuls.")
        return results
    
    def _add_api_key(self, fn):
        url = 'https://financialmodelingprep.com{functionString}'.format(functionString=fn)

        if fn[-1] != '?':
            url += '&apikey={apikey}'.format(apikey = self.api_key)
        else:
            url += 'apikey={apikey}'.format(apikey = self.api_key)
        
        return url

    def _endpoint_wrapper(self, url):
        
        response = self._FMP_api_call(url, self._max_try)
        
        return response

    def _validate_response(self, r):
        if r.status_code != 200:
            raise Exception("Error Status Code {status_code}: {Content}".format(r.status_code, r.content))
        if "Our standard API call frequency is 5 calls per minute and 500 calls per day" in str(r.content):
            raise Exception("Limit Reached.")

    def _FMP_api_call(self, url, try_ct=5):
        if try_ct == 0:
            raise Exception("Error - Max Try Reached")
        
        if self._api_call_ct == 0:
            time.sleep(self._sleep_time)
            self._api_call_ct = self._api_call_limit_per_minute
        
        try:
            r = requests.get(url)
            self._api_call_ct -= 1
            self._validate_response(r)
        except:
            r = self._FMP_api_call(url, try_ct-1)

        return r

######################################################################################################
#################################  Stock Fundamental   ################################################
######################################################################################################

    def Financial_Statement_List(self, url_only=False):
        '''
        List of symbols that have financial statements
        '''
        fn = '/api/v3/financial-statement-symbol-lists?'
        fn = self._add_api_key(fn)
        if url_only: return fn
        return self._endpoint_wrapper(fn).json()
    
    def Income_Statement(self, symbol, period=None, datatype=None, limit=120, url_only=False):
        if not symbol:
            return "Error No input symbol"
        
        fn = '/api/v3/income-statement/{symbol}?'.format(symbol=symbol)

        if period:
            fn += 'period={period}'.format(period=period)
        
        if limit:
            fn += '&limit={limit}'.format(limit=limit)

        fn = self._add_api_key(fn)
        if url_only: return fn

        if datatype == 'csv':
            return pd.DataFrame(self._endpoint_wrapper(fn).json()).set_index(['cik', 'calendarYear', 'period'])
        else:
            return self._endpoint_wrapper(fn).json()
        
    def Balance_Sheet_Statement(self, symbol, period=None, datatype=None, limit=120, url_only=False):
        if not symbol:
            return "Error"
        
        fn = '/api/v3/balance-sheet-statement/{symbol}?'.format(symbol=symbol)

        if period:
            fn += 'period={period}'.format(period=period)
        
        if limit:
            fn += '&limit={limit}'.format(limit=limit)

        fn = self._add_api_key(fn)
        if url_only: return fn

        if datatype == 'csv':
            return pd.DataFrame(self._endpoint_wrapper(fn).json()).set_index(['cik', 'calendarYear', 'period'])
        else:
            return self._endpoint_wrapper(fn).json()     

    def Cash_Flow_Statement(self, symbol, period=None, datatype=None, limit=120, url_only=False):
        if not symbol:
            return "Error"
        
        fn = '/api/v3/cash-flow-statement/{symbol}?'.format(symbol=symbol)

        if period:
            fn += 'period={period}'.format(period=period)
        
        if limit:
            fn += '&limit={limit}'.format(limit=limit)

        fn = self._add_api_key(fn)
        if url_only: return fn

        if datatype == 'csv':
            return pd.DataFrame(self._endpoint_wrapper(fn).json()).set_index(['cik', 'calendarYear', 'period'])
        else:
            return self._endpoint_wrapper(fn).json()
        
######################################################################################################
#################################  Premium Account Required   ########################################
######################################################################################################

    def Sales_Revenue_By_Segments(self, symbol, period='annual', structure='flat', url_only=False):
        '''
        Query String Parameters
        symbol : String
        period : annual | quarter
        structure : hierarchical | flat
        '''
        if not symbol:
            return "Error"
        
        fn = '/api/v4/revenue-product-segmentation?symbol={symbol}'.format(symbol=symbol)

        if period:
            fn += '&period={period}'.format(period=period)
        
        if structure:
            fn += '&structure={structure}'.format(structure=structure)
        
        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()

    def Revenue_Geographic_By_Segments(self, symbol, period='annual', structure='flat', url_only=False):
        '''
        Query String Parameters
        symbol : String
        period : annual | quarter
        structure : hierarchical | flat
        '''
        if not symbol:
            return "Error"
        
        fn = '/api/v4/revenue-geographic-segmentation?symbol={symbol}'.format(symbol=symbol)

        if period:
            fn += '&period={period}'.format(period=period)
        
        if structure:
            fn += '&structure={structure}'.format(structure=structure)
        
        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Income_Statements_Reported(self, symbol, period=None, datatype=None, limit=15, url_only=False):
        if not symbol:
            return "Error"
        
        fn = '/api/v3/income-statement-as-reported/{symbol}?'.format(symbol=symbol)

        if period:
            fn += 'period={period}'.format(period=period)
        
        if limit:
            fn += '&limit={limit}'.format(limit=limit)

        fn = self._add_api_key(fn)
        if url_only: return fn

        if datatype == 'csv':
            return pd.DataFrame(self._endpoint_wrapper(fn).json())
        else:
            return self._endpoint_wrapper(fn).json()
        
    def Balance_Sheet_Statement_Reported(self, symbol, period=None, datatype=None, limit=15, url_only=False):
        if not symbol:
            return "Error"
        
        fn = '/api/v3/balance-sheet-statement-as-reported/{symbol}?'.format(symbol=symbol)

        if period:
            fn += 'period={period}'.format(period=period)
        
        if limit:
            fn += '&limit={limit}'.format(limit=limit)

        fn = self._add_api_key(fn)
        if url_only: return fn

        if datatype == 'csv':
            return pd.DataFrame(self._endpoint_wrapper(fn).json())
        else:
            return self._endpoint_wrapper(fn).json()
        
    def Cash_Flow_Statement_Reported(self, symbol, period=None, datatype=None, limit=15, url_only=False):
        if not symbol:
            return "Error"
        
        fn = '/api/v3/cash-flow-statement-as-reported/{symbol}?'.format(symbol=symbol)

        if period:
            fn += 'period={period}'.format(period=period)
        
        if limit:
            fn += '&limit={limit}'.format(limit=limit)

        fn = self._add_api_key(fn)
        if url_only: return fn

        if datatype == 'csv':
            return pd.DataFrame(self._endpoint_wrapper(fn).json())
        else:
            return self._endpoint_wrapper(fn).json()
        
    def Full_Financial_Statement_Reported(self, symbol, period=None, url_only=False):

        if not symbol:
            return "Error"
        
        fn = '/api/v3/cash-flow-statement-as-reported/{symbol}?'.format(symbol=symbol)

        if period:
            fn += 'period={period}'.format(period=period)
        
        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()

    def International_Filings(self, exchange='EDF.PA', limit=100, url_only=False):
        fn = '/api/v3/income-statement/{exchange}?'.format(exchange=exchange)

        if limit:
            fn += 'limit={limit}'.format(limit=limit)
        
        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()

    def Quarterly_Earnings_Reports(self, symbol, year, period, url_only=False):
        '''
        period : Q1 | Q2 | Q3 | Q4
        '''
        fn = '/api/v4/financial-reports-json?symbol={symbol}'.format(symbol=symbol)

        if year:
            fn += '&year={year}'.format(year=year)

        if period:
            fn += '&period={period}'.format(period=period)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Shares_Float(self, symbol = None, url_only=False):
        if not symbol:
            fn = '/api/v4/shares_float/all'
        else:
            fn = '/api/v4/shares_float?symbol={symbol}'.format(symbol=symbol)
        
        fn = self._add_api_key(fn)
        if url_only: return fn        
        
        return self._endpoint_wrapper(fn).json()

    def Earning_Call_Transcript(self, symbol, year, quarter, url_only=False):
        '''
        Query String Parameters
        Quarter : 1 | 2 | 3 | 4
        Year : Number (ex: 2020)
        '''
        fn = '/api/v3/earning_call_transcript/{symbol}?'.format(symbol=symbol)

        if quarter:
            fn += 'quarter={quarter}'.format(quarter=quarter)
        
        if year:
            fn += '&year={year}'.format(year=year)
        
        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json() 

######################################################################################################
#################################  Stock Fundamentals Analysis  ######################################
######################################################################################################

    def Company_Financial_Ratios_ttm(self, symbol, url_only=False):
        '''
        Query String Parameters
        limit : Number
        period : annual | quarter
        '''
        fn = '/api/v3/ratios-ttm/{symbol}?'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn
        
        return self._endpoint_wrapper(fn).json()

    def Company_Financial_Ratios(self, symbol, period, limit, url_only=False):
        '''
        Query String Parameters
        limit : Number
        period : annual | quarter
        '''
        fn = '/api/v3/ratios/{symbol}?'.format(symbol=symbol)

        if period:
            fn += 'period={period}'.format(period=period)
        
        if limit:
            fn += '&year={limit}'.format(limit=limit)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()

    def Stock_Financial_Scores(self, symbol, url_only=False):
        fn = '/api/v4/score?symbol={symbol}'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Owners_Earning(self, symbol, url_only=False):
        fn = '/api/v4/owner_earnings?symbol={symbol}'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()

    def Company_Enterprise_Value(self, symbol, period, limit, url_only=False):
        fn = '/api/v3/enterprise-values/{symbol}?'.format(symbol=symbol)

        if period:
            fn += 'period={period}'.format(period=period)
        if limit:
            fn += '&limit={limit}'.format(limit=limit)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()

    def Financial_Statement_Growth(self, symbol, limit, url_only=False):
        fn = '/api/v3/income-statement-growth/{symbol}?'.format(symbol=symbol)

        if limit:
            fn += 'limit={limit}'.format(limit=limit)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Company_Key_Metrics(self, symbol, period, limit, url_only=False):
        fn = '/api/v3/key-metrics-ttm/{symbol}?'.format(symbol=symbol)

        if limit:
            fn += 'limit={limit}'.format(limit=limit)
        if period:
            fn += '&period={period}'.format(period=period)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Company_Financial_Growth(self, symbol, period, limit, url_only=False):
        fn = '/api/v3/financial-growth/{symbol}?'.format(symbol=symbol)

        if limit:
            fn += 'limit={limit}'.format(limit=limit)
        if period:
            fn += '&period={period}'.format(period=period)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()

    def Company_Rating(self, symbol, url_only=False):
        fn = '/api/v3/rating/{symbol}?'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Company_Rating_Historical(self, symbol, limit, url_only=False):
        fn = '/api/v3/historical-rating/{symbol}?limit={limit}'.format(symbol=symbol, limit=limit)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Company_DCF_Value(self, symbol, WACC, levered, url_only=False):
        if levered:
            fn = '/api/v4/advanced_levered_discounted_cash_flow?symbol={symbol}'.format(symbol=symbol)
        elif WACC:
            fn = '/api/v4/advanced_discounted_cash_flow?symbol={symbol}'.format(symbol=symbol)
        else:
            fn = '/api/v3/discounted-cash-flow/{symbol}?'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Company_DCF_Value_Historical(self, symbol, period, limit, url_only=False):
        fn = '/api/v3/historical-daily-discounted-cash-flow/{symbol}?'.format(symbol=symbol)
        
        if limit:
            fn += 'limit={limit}'.format(limit=limit)
        if period:
            fn += '&period={period}'.format(period=period)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()

######################################################################################################
#################################  Price Target    ###################################################
######################################################################################################

    def Price_Target(self, symbol, url_only=False):
        fn = '/api/v4/price-target?symbol={symbol}'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Price_Target_Summary(self, symbol, url_only=False):
        fn = '/api/v4/price-target-summary?symbol={symbol}'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Price_Target_By_Analyst_Name(self, Analyst_Name, url_only=False):
        fn = '/api/v4/price-target-analyst-name?name={Analyst_Name}'.format(Analyst_Name=Analyst_Name)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Price_Target_By_Analyst_Company(self, company, url_only=False):
        fn = '/api/v4/price-target-analyst-company?company={company}'.format(company=company)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Price_Target_Consensus(self, symbol, url_only=False):
        fn = '/api/v4/price-target-consensus?symbol={symbol}'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Upgrade_Downgrade(self, symbol, url_only=False):
        fn = '/api/v4/upgrades-downgrades?symbol={symbol}'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Upgrade_Downgrade_Consensus(self, symbol, url_only=False):
        fn = '/api/v4/upgrades-downgrades-consensus?symbol={symbol}'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Upgrade_Downgrade_By_Agency(self, agency, url_only=False):
        fn = '/api/v4/upgrades-downgrades-grading-company?company={agency}'.format(agency=agency)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
######################################################################################################
#################################  ETF and Mutual Fund Holdings   ####################################
######################################################################################################

    def Mutual_Fund_Holdings_Available_Dates(self, symbol, url_only=False):
        fn = '/api/v4/mutual-fund-holdings/portfolio-date?symbol={symbol}'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()

    def Mutual_Fund_Holdings_Historical(self, symbol, date, url_only=False):
        fn = '/api/v4/mutual-fund-holdings?symbol={symbol}&date={date}'.format(symbol=symbol, date=date)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Mutual_Fund_Holdings_Search(self, name, url_only=False):
        fn = '/api/v4/mutual-fund-holdings/name?name={name}'.format(name=name)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()    

    def ETF_Holdings_Available_Dates(self, symbol, url_only=False):
        fn = '/api/v4/etf-holdings/portfolio-date?symbol={symbol}'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()

    def ETF_Holdings_Historical(self, symbol, date, url_only=False):
        fn = '/api/v4/etf-holdings?symbol={symbol}&date={date}'.format(symbol=symbol, date=date)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()

######################################################################################################
#################################  Alternative Data   ################################################
######################################################################################################

    def Number_Of_Employees_Historical(self, symbol, url_only=False):
        fn = '/api/v4/historical/employee_count?symbol={symbol}'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()

    def Executive_Compensation(self, symbol, year, url_only=False):
        fn = '/api/v4/governance/executive_compensation?symbol={symbol}'.format(symbol=symbol)

        if year:
            fn += '&year={year}'.format(year=year)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Individual_Beneficial_Ownership(self, symbol, url_only=False):
        fn = '/api/v4/insider/ownership/acquisition_of_beneficial_ownership?symbol={symbol}'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()

######################################################################################################
#################################  Stock Calendars   #################################################
######################################################################################################

    def Earnings_Calendar(self, from_date=None, to_date=None, url_only=False):
        fn = '/api/v3/earning_calendar?'
        if not (from_date or to_date):
            return self._endpoint_wrapper(fn).json()
        
        if from_date:
            fn += 'from_date={from_date}'.format(from_date=from_date)
        
        if to_date:
            fn += '&to_date={to_date}'.format(to_date=to_date)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()   

    def Earnings_Calendar_Confirmed(self, from_date=None, to_date=None, url_only=False):
        fn = '/api/v4/earning-calendar-confirmed?'
        
        if from_date:
            fn += 'from_date={from_date}'.format(from_date=from_date)
        
        if to_date:
            fn += '&to_date={to_date}'.format(to_date=to_date)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()

    def IPO_Calendar(self, from_date=None, to_date=None, url_only=False):
        if not (from_date or to_date):
            fn = '/api/v3/ipo_calendar?'
        else:
            fn = '/api/v3/ipo_calendar?from={from_date}&to={to_date}'.format(from_date=from_date, to_date=to_date)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def IPO_Calendar_With_Prospectus(self, from_date=None, to_date=None, url_only=False):
        if not (from_date or to_date):
            fn = '/api/v3/ipo_calendar-prospectus?'
        else:
            fn = '/api/v4/ipo-calendar-prospectus?from={from_date}&to={to_date}'.format(from_date=from_date, to_date=to_date)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def IPO_Calendar_Confirmed(self, from_date=None, to_date=None, url_only=False):
        if not (from_date or to_date):
            fn = '/api/v3/ipo-calendar-confirmed?'
        else:
            fn = '/api/v4/ipo-calendar-confirmed?from={from_date}&to={to_date}'.format(from_date=from_date, to_date=to_date)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Stock_Split_Calendar(self, from_date=None, to_date=None, url_only=False):
        if not (from_date or to_date):
            fn = '/api/v3/stock_split_calendar?'
        else:
            fn = '/api/v3/stock_split_calendar?from={from_date}&to={to_date}'.format(from_date=from_date, to_date=to_date)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Dividend_Calendar(self, from_date=None, to_date=None, url_only=False):
        if not (from_date or to_date):
            fn = '/api/v3/stock_dividend_calendar?'
        else:
            fn = '/api/v3/stock_dividend_calendar?from={from_date}&to={to_date}'.format(from_date=from_date, to_date=to_date)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Dividend_Historical(self, symbol, url_only=False):
        fn = '/api/v3/historical-price-full/stock_dividend/{symbol}?'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Economic_Calendar(self, from_date=None, to_date=None, url_only=False):
        if not (from_date or to_date):
            fn = '/api/v3/economic_calendar?'
        else:
            fn = '/api/v3/economic_calendar?from={from_date}&to={to_date}'.format(from_date=from_date, to_date=to_date)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
######################################################################################################
#################################  Company Information   #############################################
######################################################################################################

    def Company_Profile(self, symbol, url_only=False):
        fn = '/api/v3/profile/{symbol}?'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Key_Executives(self, symbol, url_only=False):
        fn = '/api/v3/key-executives/{symbol}?'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Market_Capitalization(self, symbol, limit, url_only=False):
        fn = '/api/v3/key-executives/{symbol}?'.format(symbol=symbol)

        if limit:
            fn += 'limit={limit}'.format(limit=limit)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Company_Outlook(self, symbol, url_only=False):
        fn = '/api/v4/company-outlook?symbol={symbol}'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json() 

    def Stock_Peers(self, symbol, url_only=False):
        fn = '/api/v4/stock_peers?symbol={symbol}'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()   
    
    def Delisted_Companies(self, url_only=False):
        fn = '/api/v3/delisted-companies?'

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json() 
    
    def Company_Core_Information(self, symbol, datatype=None, url_only=False):
        fn = '/api/v4/company-core-information?symbol={symbol}'.format(symbol = symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        if datatype == 'csv':
            return pd.DataFrame(self._endpoint_wrapper(fn).json())
        
        return self._endpoint_wrapper(fn).json() 
    
######################################################################################################
#################################  Stock News   ######################################################
######################################################################################################

    def FMP_Articles(self, page, size, url_only=False):
        fn = '/api/v3/fmp/articles?page={page}&size={size}'.format(page=page, size=size)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json() 

    def Stock_News(self, symbol, page, limit, url_only=False):
        if not symbol:
            fn = '/api/v3/stock_news?limit={limit}'.format(limit=limit)
            return self._endpoint_wrapper(fn).json() 
        
        tickers=symbol[0] if len(symbol) == 1 else ",".join(symbol)
        fn = '/api/v3/stock_news?tickers={tickers}&limit={limit}&page={page}'.format(tickers=tickers, limit=limit, page=page)
        
        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json() 
    
    def Forex_News(self, symbol, page, url_only=False):
        if not symbol:
            fn = '/api/v4/forex_news?page={page}'.format(page=page)
            return self._endpoint_wrapper(fn).json() 
        
        tickers=symbol[0] if len(symbol) == 1 else ",".join(symbol)
        fn = '/api/v4/forex_news?symbol={tickers}&page={page}'.format(tickers=tickers, page=page)
        
        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json() 
    
    def General_News(self, page, url_only=False):
        fn = '/api/v4/general_news?page={page}'.format(page=page)
        
        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json() 
    
    def Press_Release(self, symbol, page, url_only=False):
        fn = '/api/v3/press-releases/{symbol}?page={page}'.format(symbol=symbol, page=page)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json() 
    
######################################################################################################
#################################  Market Performance   ##############################################
######################################################################################################

    def Sectors_PE_Ratio(self, date, exchange, url_only=False):
        fn = '/api/v4/sector_price_earning_ratio?date={date}&exchange={exchange}'.format(date=date, exchange=exchange)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json() 
    
    def Industries_PE_Ratio(self, date, exchange, url_only=False):
        fn = '/api/v4/industry_price_earning_ratio?date={date}&exchange={exchange}'.format(date=date, exchange=exchange)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json() 
    
    def Stock_Market_Sectors_Performance(self, limit, url_only=False):
        if not limit:
            fn = '/api/v3/sector-performance?'
        else:
            fn = '/api/v3/historical-sectors-performance?limit={limit}'.format(limit=limit)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json() 
    
    def Most_Gainer_Stock_Companies(self, url_only=False):
        fn = '/api/v3/stock_market/gainers?'

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Most_Loser_Stock_Companies(self, url_only=False):
        fn = '/api/v3/stock_market/losers?'

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()

    def Most_Active_Stock_Companies(self, url_only=False):
        fn = '/api/v3/stock_market/actives?'

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Standard_Industrial_Classification(self, symbol, url_only=False):
        fn = '/api/v4/standard_industrial_classification?symbol={symbol}'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json() 
    
    def Standard_Industrial_Classification_List(self, industryTitle, url_only=False):
        if not industryTitle:
            fn = '/api/v4/standard_industrial_classification_list?'
        else:
            fn = '/api/v4/standard_industrial_classification_list?industryTitle={industryTitle}'.format(industryTitle=industryTitle)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json() 

    def COT_Trading_Symbols_List(self, url_only=False):
        fn = '/api/v4/commitment_of_traders_report/list?'

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def COT_Report(self, symbol, from_date, to_date, url_only=False):
        if symbol:
            fn = '/api/v4/commitment_of_traders_report/{symbol}?'.format(symbol=symbol)
        else:
            fn = '/api/v4/commitment_of_traders_report?from={from_date}&to={to_date}'.format(from_date=from_date, to_date=to_date)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Commitments_of_Traders_Analysis(self, symbol, from_date, to_date, url_only=False):
        if symbol:
            fn = '/api/v4/commitment_of_traders_report_analysis/{symbol}?'.format(symbol=symbol)
        else:
            fn = '/api/v4/commitment_of_traders_report_analysis?from={from_date}&to={to_date}'.format(from_date=from_date, to_date=to_date)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
######################################################################################################
#################################  Stock Statistics   ################################################
######################################################################################################

    def Social_Sentiment(self, symbol, type, source, page, url_only=False):
        '''
        type: bullish | bearish
        source: twitter | stocktwits
        '''
        if symbol:
            fn = '/api/v4/historical/social-sentiment?symbol={symbol}&page={page}'.format(symbol=symbol, page=page)
        elif type:
            fn = '/api/v4/social-sentiments/trending?type={type}&source={source}'.format(type=type, source=source)
        else:
            fn = '/api/v4/social-sentiment/trending?'

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Stock_Grade(self, symbol, limit, url_only=False):
        fn = '/api/v3/grade/{symbol}?limit={limit}'.format(symbol=symbol, limit=limit)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Earnings_Surprises(self, symbol, url_only=False):
        fn = '/api/v3/earnings-surprises/{symbol}?'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()        
    
    def Analyst_Estimates(self, symbol, period, limit, url_only=False):
        fn = '/api/v3/analyst-estimates/{symbol}?'.format(symbol=symbol)
        if period:
            fn += 'period={period}'.format(period=period)
        if symbol:
            fn += '&symbol={symbol}'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()   
    
    def Merger_Acquisition(self, name, page, url_only=False):
        if page:
            fn = '/api/v4/mergers-acquisitions-rss-feed?page={page}'.format(page=page)
        else:
            fn = '/api/v4/mergers-acquisitions/search?name={name}'.format(name=name)
        
        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json() 
    
######################################################################################################
#################################  Insider/Senate Trading   ##########################################
######################################################################################################

    def Stock_Insider_Trading(self, symbol, page, url_only=False):
        fn = '/api/v4/insider-trading?symbol={symbol}&page={page}'.format(symbol=symbol, page=page)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json() 

    def Senate_Trading(self, symbol, page, rss, url_only=False):
        if rss:
            fn = '/api/v4/senate-trading-rss-feed?page={page}'.format(page=page)
        else:
            fn = '/api/v4/senate-trading?symbol={symbol}'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json() 

    def Senate_Disclosure(self, symbol, page, rss, url_only=False):
        if rss:
            fn = '/api/v4/senate-disclosure-rss-feed?page={page}'.format(page=page)
        else:
            fn = '/api/v4/senate-disclosure?symbol={symbol}'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
######################################################################################################
#################################  Economics   #######################################################
######################################################################################################

    def Market_Risk_Premium(self, url_only=False):
        fn = '/api/v4/market_risk_premium?'

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()

    def Treasure_Rates(self, from_date, to_date, url_only=False):
        fn = '/api/v4/treasury?from={from_date}&to={to_date}'.format(from_date=from_date, to_date=to_date)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()

    def Economic_Indicator(self, name, from_date, to_date, url_only=False):
        '''
        GDP | realGDP | nominalPotentialGDP | realGDPPerCapita | federalFunds | CPI | inflationRate | inflation | retailSales | consumerSentiment 
        durableGoods | unemploymentRate | totalNonfarmPayroll | initialClaims | industrialProductionTotalIndex | 
        newPrivatelyOwnedHousingUnitsStartedTotalUnits | totalVehicleSales | retailMoneyFunds | smoothedUSRecessionProbabilities | 
        3MonthOr90DayRatesAndYieldsCertificatesOfDeposit | commercialBankInterestRateOnCreditCardPlansAllAccounts | 
        30YearFixedRateMortgageAverage | 15YearFixedRateMortgageAverage
        '''
        fn = '/api/v4/economic?name={name}&from={from_date}&to={to_date}'.format(name=name, from_date=from_date, to_date=to_date)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
######################################################################################################
#################################  Stock Price   #####################################################
######################################################################################################

    def Companies_Quote(self, symbol, otc=False, url_only=False):
        tickers = symbol[0] if len(symbol) == 1 else ",".join(symbol)
        if otc:
            fn = '/api/v3/otc/real-time-price/{tickers}?'.format(tickers=tickers)
        else:
            fn = '/api/v3/quote/{tickers}?'.format(tickers=tickers)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()

    def Stock_Price_Change(self, symbol, url_only=False):
        tickers = symbol[0] if len(symbol) == 1 else ",".join(symbol)
        fn = '/api/v3/stock-price-change/{tickers}?'.format(tickers=tickers)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Stock_Price(self, symbol, url_only=False):
        fn = '/api/v3/quote-short/{symbol}?'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Stock_Price_List(self, exchange, url_only=False):
        fn = '/api/v3/quotes/{exchange}?'.format(exchange=exchange)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Stock_Price_Historical_With_Volume(self, symbol, interval, url_only=False):
        fn = '/api/v3/historical-chart/{interval}/{symbol}?'.format(interval=interval, symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Daily_Indicators(self, symbol, period, type, url_only=False):
        '''
        type: SMA - EMA - WMA - DEMA - TEMA - williams - RSI - ADX - standardDeviation
        '''
        fn = '/api/v3/technical_indicator/daily/{symbol}?period={period}&type={type}'.format(symbol=symbol, period=period, type=type)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
######################################################################################################
#################################  Fund Holdings   ###################################################
######################################################################################################

    def ETF_Holdings(self, symbol, url_only=False):
        fn = '/api/v3/etf-holder/{symbol}?'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def ETF_Expense_Ratio(self, symbol, url_only=False):
        fn = '/api/v4/etf-info?symbol={symbol}'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Institutional_Holders(self, symbol, url_only=False):
        fn = '/api/v3/institutional-holder/{symbol}?'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()        
    
    def Mutual_Fund_Holders(self, symbol, url_only=False):
        fn = '/api/v3/mutual-fund-holder/{symbol}?'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()      

    def ETF_Sector_Weightings(self, symbol, url_only=False):
        fn = '/api/v3/etf-sector-weightings/{symbol}?'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()  
    
    def ETF_Country_Weightings(self, symbol, url_only=False):
        fn = '/api/v3/etf-country-weightings/{symbol}?'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()  
    
    def ETF_Stock_Exposure(self, symbol, url_only=False):
        fn = '/api/v3/etf-stock-exposure/{symbol}?'.format(symbol=symbol)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()  
    
    def Complete_Cik_List(self, url_only=False):
        fn = '/api/v3/cik_list?'

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()  
    
    def Search_Cik_By_Name(self, name, url_only=False):
        fn = '/api/v3/cik-search/{name}?'.format(name=name)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Search_Name_By_Cik(self, cik, url_only=False):
        fn = '/api/v3/cik/{cik}?'.format(cik=cik)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Institutional_Manager_Positions(self, cik, date, url_only=False):
        fn = '/api/v3/form-thirteen/{cik}?date={date}'.format(cik=cik, date=date)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Symbols_List(self, url_only=False):
        fn = '/api/v3/stock/list?'

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()

    def ETF_List(self, url_only=False):
        fn = '/api/v3/etf/list?'

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json() 
    
######################################################################################################
#################################  Market Indexes   ##################################################
######################################################################################################

    def Major_Indexes(self, url_only=False):
        fn = '/api/v3/quotes/index?'

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json() 

    def Sp500_Constituents(self, datatype='json', url_only=False):

        fn = '/api/v3/sp500_constituent?'

        fn = self._add_api_key(fn)
        if url_only: return fn

        if datatype=='csv':
            return pd.DataFrame(self._endpoint_wrapper(fn).json())
        else:
            return self._endpoint_wrapper(fn).json() 
        
    def Sp500_Constituents_Historical(self, url_only=False):
        fn = '/api/v3/historical/sp500_constituent?'

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Nasdaq_100(self, datatype='json', url_only=False):

        fn = '/api/v3/nasdaq_constituent?'

        fn = self._add_api_key(fn)
        if url_only: return fn

        if datatype=='csv':
            return pd.DataFrame(self._endpoint_wrapper(fn).json())
        else:
            return self._endpoint_wrapper(fn).json() 
        
    def Nasdaq_100_Historical(self, url_only=False):
        fn = '/api/v3/historical/nasdaq_constituent?'

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def DJ_Constituents(self, datatype='json', url_only=False):
        fn = '/api/v3/dowjones_constituent?'

        fn = self._add_api_key(fn)
        if url_only: return fn

        if datatype=='csv':
            return pd.DataFrame(self._endpoint_wrapper(fn).json())
        else:
            return self._endpoint_wrapper(fn).json() 
        
    def DJ_Constituents_Historical(self, url_only=False):
        fn = '/api/v3/historical/dowjones_constituent?'

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def FX_Rate(self, url_only=False):
        fn = '/api/v3/fx?'

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()

    def FX_Quotes(self, url_only=False):
        fn = '/api/v3/quotes/forex?'

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()

    def FX_Rate_By_Pair(self, currency_pair, url_only=False):
        fn = '/api/v3/fx/{currency_pair}?'.format(currency_pair=currency_pair)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()

    def FX_Quotes_By_Pair(self, currency_pair, url_only=False):
        fn = '/api/v3/quote/{currency_pair}?'.format(currency_pair=currency_pair)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def FX_Quotes_By_Pair_Historical(self, currency_pair, interval, url_only=False):
        fn = '/api/v3/historical-chart/{interval}/{currency_pair}?'.format(interval=interval, currency_pair=currency_pair)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Commodities_Prices_All(self, url_only=False):
        fn = '/api/v3/quotes/commodity?'

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()
    
    def Commodities_Prices_Historical(self, comm, interval, url_only=False):
        fn = '/api/v3/historical-chart/{interval}/{comm}?'.format(interval=interval, comm=comm)

        fn = self._add_api_key(fn)
        if url_only: return fn

        return self._endpoint_wrapper(fn).json()       

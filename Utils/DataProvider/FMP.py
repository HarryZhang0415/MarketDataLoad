from Utils.DataProvider import mysql_config, api_key_sql
import mysql.connector
import requests
import pandas as pd
import datetime
import io

class FMP(object):

    def __init__(self) -> None:
        cnx = mysql.connector.connect(**mysql_config)
        cursor = cnx.cursor()
        cursor.execute(api_key_sql, [FMP.__name__, FMP.__name__])

        for _ in cursor:
            self.api_key = _[0]

        try: 
            url = 'https://site.financialmodelingprep.com/developer/docs'
            request = requests.get(url, timeout=5)
            print('FMP Connection Established')
        except:
            print("FMP Connection Failed")

    def _FMP_api_call(self, fn):
        url = 'https://financialmodelingprep.com{functionString}'.format(functionString=fn)

        if fn[-1] != '?':
            url += '&apikey={apikey}'.format(apikey = self.api_key)
        else:
            url += 'apikey={apikey}'.format(apikey = self.api_key)

        r = requests.get(url)

        return r

######################################################################################################
#################################  Stock Fundamental   ################################################
######################################################################################################

    def Financial_Statement_List(self):
        '''
        List of symbols that have financial statements
        '''
        fn = '/api/v3/financial-statement-symbol-lists?'
        return self._FMP_api_call(fn).json()
    
    def Income_Statement(self, symbol, period=None, datatype=None, limit=120):
        if not symbol:
            return "Error No input symbol"
        
        fn = '/api/v3/income-statement/{symbol}?'.format(symbol)

        if period:
            fn += 'period={period}'.format(period)
        
        if limit:
            fn += '&limit={limit}'.format(limit)

        if datatype == 'csv':
            fn += '&datatype={datatype}'.format(datatype)
            r = self._FMP_api_call(fn)
            return pd.read_csv(io.StringIO(r.content.decode('utf-8')))
        else:
            return self._FMP_api_call(fn).json()
        
    def Balance_Sheet_Statement(self, symbol, period=None, datatype=None, limit=120):
        if not symbol:
            return "Error"
        
        fn = '/api/v3/balance-sheet-statement/{symbol}?'.format(symbol)

        if period:
            fn += 'period={period}'.format(period)
        
        if limit:
            fn += '&limit={limit}'.format(limit)

        if datatype == 'csv':
            fn += '&datatype={datatype}'.format(datatype)
            r = self._FMP_api_call(fn)
            return pd.read_csv(io.StringIO(r.content.decode('utf-8')))
        else:
            return self._FMP_api_call(fn).json()       

    def Cash_Flow_Statement(self, symbol, period=None, datatype=None, limit=120):
        if not symbol:
            return "Error"
        
        fn = '/api/v3/cash-flow-statement/{symbol}?'.format(symbol)

        if period:
            fn += 'period={period}'.format(period)
        
        if limit:
            fn += '&limit={limit}'.format(limit)

        if datatype == 'csv':
            fn += '&datatype={datatype}'.format(datatype)
            r = self._FMP_api_call(fn)
            return pd.read_csv(io.StringIO(r.content.decode('utf-8')))
        else:
            return self._FMP_api_call(fn).json()
        
######################################################################################################
#################################  Premium Account Required   ########################################
######################################################################################################

    def Sales_Revenue_By_Segments(self, symbol, period='annual', structure='flat'):
        '''
        Query String Parameters
        symbol : String
        period : annual | quarter
        structure : hierarchical | flat
        '''
        if not symbol:
            return "Error"
        
        fn = '/api/v4/revenue-product-segmentation?symbol={symbol}?'.format(symbol)

        if period:
            fn += 'period={period}'.format(period)
        
        if structure:
            fn += 'structure={structure}'.format(structure)
        

        return self._FMP_api_call(fn).json()

    def Revenue_Geographic_By_Segments(self, symbol, period='annual', structure='flat'):
        '''
        Query String Parameters
        symbol : String
        period : annual | quarter
        structure : hierarchical | flat
        '''
        if not symbol:
            return "Error"
        
        fn = '/api/v4/revenue-product-segmentation?symbol={symbol}?'.format(symbol)

        if period:
            fn += 'period={period}'.format(period)
        
        if structure:
            fn += 'structure={structure}'.format(structure)
        

        return self._FMP_api_call(fn).json()
    
    def Income_Statements_Reported(self, symbol, period=None, datatype=None, limit=15):
        if not symbol:
            return "Error"
        
        fn = '/api/v3/income-statement-as-reported/{symbol}?'.format(symbol)

        if period:
            fn += 'period={period}'.format(period)
        
        if limit:
            fn += '&limit={limit}'.format(limit)

        if datatype == 'csv':
            fn += '&datatype={datatype}'.format(datatype)
            r = self._FMP_api_call(fn)
            return pd.read_csv(io.StringIO(r.content.decode('utf-8')))
        else:
            return self._FMP_api_call(fn).json()
        
    def Balance_Sheet_Statement_Reported(self, symbol, period=None, datatype=None, limit=15):
        if not symbol:
            return "Error"
        
        fn = '/api/v3/balance-sheet-statement-as-reported/{symbol}?'.format(symbol)

        if period:
            fn += 'period={period}'.format(period)
        
        if limit:
            fn += '&limit={limit}'.format(limit)

        if datatype == 'csv':
            fn += '&datatype={datatype}'.format(datatype)
            r = self._FMP_api_call(fn)
            return pd.read_csv(io.StringIO(r.content.decode('utf-8')))
        else:
            return self._FMP_api_call(fn).json()
        
    def Cash_Flow_Statement_Reported(self, symbol, period, datatype, limit):
        if not symbol:
            return "Error"
        
        fn = '/api/v3/cash-flow-statement-as-reported/{symbol}?'.format(symbol)

        if period:
            fn += 'period={period}'.format(period)
        
        if limit:
            fn += '&limit={limit}'.format(limit)

        if datatype == 'csv':
            fn += '&datatype={datatype}'.format(datatype)
            r = self._FMP_api_call(fn)
            return pd.read_csv(io.StringIO(r.content.decode('utf-8')))
        else:
            return self._FMP_api_call(fn).json()
        
    def Full_Financial_Statement_Reported(self, symbol, period):

        if not symbol:
            return "Error"
        
        fn = '/api/v3/cash-flow-statement-as-reported/{symbol}?'.format(symbol)

        if period:
            fn += 'period={period}'.format(period)
        
        return self._FMP_api_call(fn).json()

    def International_Filings(self, exchange, limit):
        fn = '/api/v3/income-statement/{exchange}?'.format(exchange)

        if limit:
            fn += 'limit={limit}'.format(limit)
        
        return self._FMP_api_call(fn).json()

    def Quarterly_Earnings_Reports(self, symbol, year, period):
        fn = '/api/v4/financial-reports-json?symbol={symbol}?'.format(symbol)

        if year:
            fn += '&year={year}'.format(year)

        if period:
            fn += '&year={year}'.format(period)
        
        return self._FMP_api_call(fn).json()
    
    def Shares_Float(self, symbol):
        if not symbol:
            fn = '/api/v4/shares_float/all'
        else:
            fn = '/api/v4/shares_float?symbol={symbol}?'.format(symbol)
        
        return self._FMP_api_call(fn).json()

    def Earning_Call_Transcript(self, symbol, year, quarter):
        fn = '/api/v3/earning_call_transcript/{symbol}?'.format(symbol)

        if quarter:
            fn += 'quarter={quarter}'.format(quarter)
        
        if year:
            fn += '&year={year}'.format(year)
        
        return self._FMP_api_call(fn).json()        

######################################################################################################
#################################  Stock Fundamentals Analysis  ######################################
######################################################################################################

    def Company_Financial_Ratios(self, symbol, period, limit):
        fn = '/api/v3/ratios-ttm/{symbol}?'.format(symbol)

        if period:
            fn += 'period={period}'.format(period)
        
        if limit:
            fn += '&year={limit}'.format(limit)
        
        return self._FMP_api_call(fn).json()

    def Stock_Financial_Scores(self, symbol):
        fn = '/api/v4/score?symbol={symbol}?'.format(symbol)
        
        return self._FMP_api_call(fn).json()  
    
    def Owners_Earning(self, symbol):
        fn = '/api/v4/owner_earnings?symbol={symbol}?'.format(symbol)
        
        return self._FMP_api_call(fn).json() 

    def Company_Enterprise_Value(self, symbol, period, limit):
        fn = '/api/v3/enterprise-values/{symbol}?'.format(symbol)

        if period:
            fn += 'period={period}'.format(period)
        if limit:
            fn += '&limit={limit}'.format(limit)
        
        return self._FMP_api_call(fn).json()

    def Financial_Statement_Growth(self, symbol, limit):
        fn = '/api/v3/income-statement-growth/{symbol}?'.format(symbol)

        if limit:
            fn += 'limit={limit}'.format(limit)
        
        return self._FMP_api_call(fn).json()
    
    def Company_Key_Metrics(self, symbol, period, limit):
        fn = '/api/v3/key-metrics-ttm/{symbol}?'.format(symbol)

        if limit:
            fn += 'limit={limit}'.format(limit)
        if period:
            fn += '&period={period}'.format(period)
        
        return self._FMP_api_call(fn).json()
    
    def Company_Financial_Growth(self, symbol, period, limit):
        fn = '/api/v3/financial-growth/{symbol}?'.format(symbol)

        if limit:
            fn += 'limit={limit}'.format(limit)
        if period:
            fn += '&period={period}'.format(period)
        
        return self._FMP_api_call(fn).json()

    def Company_Rating(self, symbol):
        fn = '/api/v3/rating/{symbol}?'.format(symbol)
        
        return self._FMP_api_call(fn).json()
    
    def Company_Rating_Historical(self, symbol, limit):
        fn = '/api/v3/historical-rating/{symbol}?limit={limit}'.format(symbol, limit)
        
        return self._FMP_api_call(fn).json()
    
    def Company_DCF_Value(self, symbol, WACC, levered):
        if levered:
            fn = '/api/v4/advanced_levered_discounted_cash_flow?symbol={symbol}?'.format(symbol)
        elif WACC:
            fn = '/api/v4/advanced_discounted_cash_flow?symbol={symbol}?'.format(symbol)
        else:
            fn = '/api/v3/discounted-cash-flow/{symbol}?'.format(symbol)
        
        return self._FMP_api_call(fn).json()
    
    def Company_DCF_Value_Historical(self, symbol, period, limit):
        fn = '/api/v3/historical-daily-discounted-cash-flow/{symbol}?'.format(symbol)
        
        if limit:
            fn += 'limit={limit}'.format(limit)
        if period:
            fn += '&period={period}'.format(period)

        return self._FMP_api_call(fn).json()

######################################################################################################
#################################  Price Target    ###################################################
######################################################################################################

    def Price_Target(self, symbol):
        fn = '/api/v4/price-target?symbol={symbol}?'.format(symbol)

        return self._FMP_api_call(fn).json()
    
    def Price_Target_Summary(self, symbol):
        fn = '/api/v4/price-target-summary?symbol={symbol}?'.format(symbol)

        return self._FMP_api_call(fn).json()
    
    def Price_Target_By_Analyst_Name(self, Analyst_Name):
        fn = '/api/v4/price-target-analyst-name?name={Analyst_Name}?'.format(Analyst_Name)

        return self._FMP_api_call(fn).json()
    
    def Price_Target_By_Analyst_Company(self, company):
        fn = '/api/v4/price-target-analyst-company?company={company}?'.format(company)

        return self._FMP_api_call(fn).json()
    
    def Price_Target_Consensus(self, symbol):
        fn = '/api/v4/price-target-consensus?symbol={symbol}?'.format(symbol)

        return self._FMP_api_call(fn).json()
    
    def Upgrade_Downgrade(self, symbol):
        fn = '/api/v4/upgrades-downgrades?symbol={symbol}?'.format(symbol)

        return self._FMP_api_call(fn).json()
    
    def Upgrade_Downgrade_Consensus(self, symbol):
        fn = '/api/v4/upgrades-downgrades-consensus?symbol={symbol}?'.format(symbol)

        return self._FMP_api_call(fn).json()
    
    def Upgrade_Downgrade_By_Agency(self, agency):
        fn = '/api/v4/upgrades-downgrades-grading-company?company={agency}?'.format(agency)

        return self._FMP_api_call(fn).json()
    
######################################################################################################
#################################  ETF and Mutual Fund Holdings   ####################################
######################################################################################################

    def Mutual_Fund_Holdings_Historical(self, symbol, date):
        fn = '/api/v4/mutual-fund-holdings?symbol={symbol}&date={date}'.format(symbol, date)

        return self._FMP_api_call(fn).json()
    
    def ETF_Holdings_Historical(self, symbol, date):
        fn = '/api/v4/etf-holdings/portfolio-date?symbol={symbol}&date={date}'.format(symbol, date)

        return self._FMP_api_call(fn).json()

######################################################################################################
#################################  Alternative Data   ################################################
######################################################################################################

    def Number_Of_Employees_Historical(self, symbol):
        fn = '/api/v4/historical/employee_count?symbol={symbol}'.format(symbol)

        return self._FMP_api_call(fn).json()

    def Executive_Compensation(self, symbol, year):
        fn = '/api/v4/governance/executive_compensation?symbol={symbol}'.format(symbol)

        if year:
            fn += '&year={year}'.format(year)

        return self._FMP_api_call(fn).json()
    
    def Individual_Beneficial_Ownership(self, symbol):
        fn = '/api/v4/insider/ownership/acquisition_of_beneficial_ownership?symbol={symbol}'.format(symbol)

        return self._FMP_api_call(fn).json()

######################################################################################################
#################################  Stock Calendars   #################################################
######################################################################################################

    def Earnings_Calendar(self, from_date, to_date):
        fn = '/api/v3/earning_calendar?'
        if not (from_date or to_date):
            return self._FMP_api_call(fn).json()
        
        if from_date:
            fn += 'from_date={from_date}'.format(from_date)
        
        if to_date:
            fn += '&to_date={to_date}'.format(to_date)

        return self._FMP_api_call(fn).json()   

    def Earnings_Calendar_Confirmed(self, from_date, to_date):
        fn = '/api/v4/earning-calendar-confirmed?'
        
        if from_date:
            fn += 'from_date={from_date}'.format(from_date)
        
        if to_date:
            fn += '&to_date={to_date}'.format(to_date)

        return self._FMP_api_call(fn).json()

    def IPO_Calendar(self, from_date, to_date):
        fn = '/api/v3/ipo_calendar?from={from_date}&to={to_date}'.format(from_date, to_date)

        return self._FMP_api_call(fn).json()
    
    def IPO_Calendar_With_Prospectus(self, from_date, to_date):
        fn = '/api/v4/ipo-calendar-prospectus?from={from_date}&to={to_date}'.format(from_date, to_date)

        return self._FMP_api_call(fn).json()
    
    def IPO_Calendar_Confirmed(self, from_date, to_date):
        fn = '/api/v4/ipo-calendar-confirmed?from={from_date}&to={to_date}'.format(from_date, to_date)

        return self._FMP_api_call(fn).json()
    
    def Stock_Split_Calendar(self, from_date, to_date):
        fn = '/api/v3/stock_split_calendar?from={from_date}&to={to_date}'.format(from_date, to_date)

        return self._FMP_api_call(fn).json()
    
    def Dividend_Calendar(self, from_date, to_date):
        fn = '/api/v3/stock_dividend_calendar?from={from_date}&to={to_date}'.format(from_date, to_date)

        return self._FMP_api_call(fn).json()
    
    def Dividend_Historical(self, symbol):
        fn = '/api/v3/historical-price-full/stock_dividend/{symbol}'.format(symbol)

        return self._FMP_api_call(fn).json()
    
    def Economic_Calendar(self, from_date, to_date):
        fn = '/api/v3/economic_calendar?from={from_date}&to={to_date}'.format(from_date, to_date)

        return self._FMP_api_call(fn).json()
    
######################################################################################################
#################################  Company Information   #############################################
######################################################################################################

    def Company_Profile(self, symbol):
        fn = '/api/v3/profile/{symbol}?'.format(symbol)

        return self._FMP_api_call(fn).json()
    
    def Key_Executives(self, symbol):
        fn = '/api/v3/key-executives/{symbol}?'.format(symbol)

        return self._FMP_api_call(fn).json()
    
    def Market_Capitalization(self, symbol, limit):
        fn = '/api/v3/key-executives/{symbol}?'.format(symbol)

        if limit:
            fn += 'limit={limit}'.format(limit)

        return self._FMP_api_call(fn).json()
    
    def Company_Outlook(self, symbol):
        fn = '/api/v4/company-outlook?symbol={symbol}?'.format(symbol)

        return self._FMP_api_call(fn).json() 

    def Stock_Peers(self, symbol):
        fn = '/api/v4/stock_peers?symbol={symbol}?'.format(symbol)

        return self._FMP_api_call(fn).json()   
    
    def Delisted_Companies(self):
        fn = '/api/v3/delisted-companies?'

        return self._FMP_api_call(fn).json() 
    
######################################################################################################
#################################  Stock News   ######################################################
######################################################################################################

    def FMP_Articles(self, page, size):
        fn = '/api/v3/fmp/articles?page={page}&size={size}'.format(page, size)

        return self._FMP_api_call(fn).json() 

    def Stock_News(self, symbol, page, limit):
        if not symbol:
            fn = '/api/v3/stock_news?limit={limit}'.format(limit)
            return self._FMP_api_call(fn).json() 
        
        tickers=symbol if len(symbol) == 1 else ",".join(symbol)
        fn = '/api/v3/stock_news?tickers={tickers}&limit={limit}&page={page}'.format(tickers, limit, page)
        

        return self._FMP_api_call(fn).json() 
    
    def Forex_News(self, symbol, page):
        if not symbol:
            fn = '/api/v4/forex_news?page={page}'.format(page)
            return self._FMP_api_call(fn).json() 
        
        tickers=symbol if len(symbol) == 1 else ",".join(symbol)
        fn = '/api/v4/forex_news?symbol={tickers}&page={page}'.format(tickers, page)
        
        return self._FMP_api_call(fn).json() 
    
    def General_News(self, page):
        fn = '/api/v4/general_news?page={page}'.format(page)
        
        return self._FMP_api_call(fn).json() 
    
    def Press_Release(self, symbol, page):
        fn = '/api/v3/press-releases/{symbol}?page={page}'.format(symbol, page)

        return self._FMP_api_call(fn).json() 
    
######################################################################################################
#################################  Market Performance   ##############################################
######################################################################################################

    def Sectors_PE_Ratio(self, date, exchange):
        fn = '/api/v4/sector_price_earning_ratio?date={date}&exchange={exchange}'.format(date=date, exchange=exchange)

        return self._FMP_api_call(fn).json() 
    
    def Industries_PE_Ratio(self, date, exchange):
        fn = '/api/v4/industry_price_earning_ratio?date={date}&exchange={exchange}'.format(date=date, exchange=exchange)

        return self._FMP_api_call(fn).json() 
    
    def Stock_Market_Sectors_Performance(self, limit):
        if not limit:
            fn = '/api/v3/sector-performance'
        else:
            fn = '/api/v3/historical-sectors-performance?limit={limit}'.format(limit)

        return self._FMP_api_call(fn).json() 
    
    def Most_Gainer_Stock_Companies(self):
        fn = '/api/v3/stock_market/gainers'

        return self._FMP_api_call(fn).json()
    
    def Most_Loser_Stock_Companies(self):
        fn = '/api/v3/stock_market/losers'

        return self._FMP_api_call(fn).json()

    def Most_Active_Stock_Companies(self):
        fn = '/api/v3/stock_market/actives'

        return self._FMP_api_call(fn).json()
    
    def Standard_Industrial_Classification(self, symbol):
        fn = '/api/v4/standard_industrial_classification?symbol={symbol}'.format(symbol)

        return self._FMP_api_call(fn).json() 
    
    def Standard_Industrial_Classification_List(self, industryTitle):
        if not industryTitle:
            fn = '/api/v4/standard_industrial_classification_list'
        else:
            fn = '/api/v4/standard_industrial_classification_list?industryTitle={industryTitle}'.format(industryTitle)

        return self._FMP_api_call(fn).json() 

    def COT_Trading_Symbols_List(self):
        fn = '/api/v4/commitment_of_traders_report/list'

        return self._FMP_api_call(fn).json()
    
    def COT_Report(self, symbol, from_date, to_date):
        if symbol:
            fn = '/api/v4/commitment_of_traders_report/{symbol}'.format(symbol)
        else:
            fn = '/api/v4/commitment_of_traders_report?from={from_date}&to={to_date}'.format(from_date, to_date)

        return self._FMP_api_call(fn).json()
    
    def Commitments_of_Traders_Analysis(self, symbol, from_date, to_date):
        if symbol:
            fn = '/api/v4/commitment_of_traders_report_analysis/{symbol}'.format(symbol)
        else:
            fn = '/api/v4/commitment_of_traders_report_analysis?from={from_date}&to={to_date}'.format(from_date, to_date)

        return self._FMP_api_call(fn).json()
    
######################################################################################################
#################################  Stock Statistics   ################################################
######################################################################################################

    def Social_Sentiment(self, symbol, type, source, page ):
        if symbol:
            fn = '/api/v4/historical/social-sentiment?symbol={symbol}&page={page}'.format(symbol, page)
        elif type:
            fn = '/api/v4/social-sentiments/trending?type={type}&source={source}'.format(type, source)
        else:
            fn = '/api/v4/social-sentiment/trending'

        return self._FMP_api_call(fn).json()
    
    def Stock_Grade(self, symbol, limit):
        fn = '/api/v3/grade/{symbol}?limit={limit}'.format(symbol, limit)

        return self._FMP_api_call(fn).json()
    
    def Earnings_Surprises(self, symbol):
        fn = '/api/v3/earnings-surprises/{symbol}?'.format(symbol)

        return self._FMP_api_call(fn).json()        
    
    def Analyst_Estimates(self, symbol, period, limit):
        fn = '/api/v3/analyst-estimates/{symbol}?'.format(symbol)
        if period:
            fn += 'period={period}'.format(period)
        if symbol:
            fn += '&symbol={symbol}'.format(symbol)

        return self._FMP_api_call(fn).json()   
    
    def Merger_Acquisition(self, name, page):
        if page:
            fn = '/api/v4/mergers-acquisitions-rss-feed?page={page}'.format(page)
        else:
            fn = '/api/v4/mergers-acquisitions/search?name={name}'.format(name)
        
        return self._FMP_api_call(fn).json() 
    
######################################################################################################
#################################  Insider/Senate Trading   ##########################################
######################################################################################################

    def Stock_Insider_Trading(self, symbol, page):
        fn = '/api/v4/insider-trading?symbol={symbol}&page={page}'.format(symbol, page)
        
        return self._FMP_api_call(fn).json() 

    def Stock_Insider_Trading(self, symbol, page, rss):
        if rss:
            fn = '/api/v4/senate-trading-rss-feed?page={page}'.format(page)
        else:
            fn = '/api/v4/senate-trading?symbol={symbol}'.format(symbol)
        
        return self._FMP_api_call(fn).json() 

    def Senate_Disclosure(self, symbol, page, rss):
        if rss:
            fn = '/api/v4/senate-disclosure-rss-feed?page={page}'.format(page)
        else:
            fn = '/api/v4/senate-disclosure?symbol={symbol}'.format(symbol)
        
        return self._FMP_api_call(fn).json()
    
######################################################################################################
#################################  Economics   #######################################################
######################################################################################################

    def Market_Risk_Premium(self):
        fn = '/api/v4/market_risk_premium'
        
        return self._FMP_api_call(fn).json()

    def Treasure_Rates(self, from_date, to_date):
        fn = '/api/v4/treasury?from={from_date}&to={to_date}'.format(from_date, to_date)
        
        return self._FMP_api_call(fn).json()

    def Economic_Indicator(self, name, from_date, to_date):
        fn = '/api/v4/economic?name={name}}&from={from_date}&to={to_date}'.format(name, from_date, to_date)
        
        return self._FMP_api_call(fn).json()

######################################################################################################
#################################  Stock Price   #####################################################
######################################################################################################

    def Companies_Quote(self, symbol, otc=False):
        tickers = symbol if len(symbol) == 1 else ",".join(symbol)
        if otc:
            fn = '/api/v3/otc/real-time-price/{tickers}'.format(tickers)
        else:
            fn = '/api/v3/quote/{tickers}'.format(tickers)
        
        return self._FMP_api_call(fn).json()

    def Stock_Price_Change(self, symbol):
        tickers = symbol if len(symbol) == 1 else ",".join(symbol)
        fn = '/api/v3/stock-price-change/{tickers}'.format(tickers)

        return self._FMP_api_call(fn).json()
    
    def Stock_Price(self, symbol):
        fn = '/api/v3/quote-short/{symbol}'.format(symbol)

        return self._FMP_api_call(fn).json()
    
    def Stock_Price_List(self, exchange):
        fn = '/api/v3/quotes/{exchange}'.format(exchange)

        return self._FMP_api_call(fn).json()
    
    def Stock_Price_Historical_With_Volume(self, symbol, interval):
        fn = '/api/v3/historical-chart/{interval}/{symbol}'.format(interval, symbol)

        return self._FMP_api_call(fn).json()
    
    def Daily_Indicators(self, symbol, period, type):
        fn = '/api/v3/technical_indicator/daily/{symbol}?period={period}&type={type}'.format(symbol, period, type)

        return self._FMP_api_call(fn).json()
    
######################################################################################################
#################################  Fund Holdings   ###################################################
######################################################################################################

    def ETF_Holdings(self, symbol):
        fn = '/api/v3/etf-holder/{symbol}'.format(symbol)

        return self._FMP_api_call(fn).json()
    
    def ETF_Expense_Ratio(self, symbol):
        fn = '/api/v4/etf-info?symbol={symbol}'.format(symbol)

        return self._FMP_api_call(fn).json()
    
    def Institutional_Holders(self, symbol):
        fn = '/api/v3/institutional-holder/{symbol}'.format(symbol)

        return self._FMP_api_call(fn).json()        
    
    def Mutual_Fund_Holders(self, symbol):
        fn = '/api/v3/mutual-fund-holder/{symbol}'.format(symbol)

        return self._FMP_api_call(fn).json()      

    def ETF_Sector_Weightings(self, symbol):
        fn = '/api/v3/etf-sector-weightings/{symbol}'.format(symbol)

        return self._FMP_api_call(fn).json()  
    
    def ETF_Country_Weightings(self, symbol):
        fn = '/api/v3/etf-country-weightings/{symbol}'.format(symbol)

        return self._FMP_api_call(fn).json()  
    
    def ETF_Stock_Exposure(self, symbol):
        fn = '/api/v3/etf-stock-exposure/{symbol}'.format(symbol)

        return self._FMP_api_call(fn).json()  
    
    def Complete_Cik_List(self):
        fn = '/api/v3/cik_list'

        return self._FMP_api_call(fn).json()  
    
    def Search_Cik_By_Name(self, name):
        fn = '/api/v3/cik-search/{name}'.format(name)

        return self._FMP_api_call(fn).json()
    
    def Search_Name_By_Cik(self, cik):
        fn = '/api/v3/cik/{cik}'.format(cik)

        return self._FMP_api_call(fn).json()
    
    def Institutional_Manager_Positions(self, cik, date):
        fn = '/api/v3/form-thirteen/{cik}?date={date}'.format(cik, date)

        return self._FMP_api_call(fn).json()
    
    def Symbols_List(self):
        fn = '/api/v3/stock/list'

        return self._FMP_api_call(fn).json()

    def ETF_List(self):
        fn = '/api/v3/etf/list'

        return self._FMP_api_call(fn).json() 
    
######################################################################################################
#################################  Mraket Indexes   ##################################################
######################################################################################################

    def Major_Indexes(self):
        fn = '/api/v3/quotes/index'

        return self._FMP_api_call(fn).json() 

    def Sp500_Constituents(self, datatype):

        fn = '/api/v3/sp500_constituent'

        if datatype=='csv':
            fn += 'datatype={datatype}'.format(datatype)
            r = self._FMP_api_call(fn)
            return pd.read_csv(io.StringIO(r.content.decode('utf-8')))
        else:
            return self._FMP_api_call(fn).json() 
        
    def Sp500_Constituents_Historical(self):
        fn = '/api/v3/historical/sp500_constituent'

        return self._FMP_api_call(fn).json()
    
    def Nasdaq_100(self, datatype):

        fn = '/api/v3/nasdaq_constituent?'

        if datatype=='csv':
            fn += 'datatype={datatype}'.format(datatype)
            r = self._FMP_api_call(fn)
            return pd.read_csv(io.StringIO(r.content.decode('utf-8')))
        else:
            return self._FMP_api_call(fn).json() 
        
    def Nasdaq_100_Historical(self):
        fn = '/api/v3/historical/nasdaq_constituent?'

        return self._FMP_api_call(fn).json()
    
    def DJ_Constituents(self, datatype):
        fn = '/api/v3/dowjones_constituent?'

        if datatype=='csv':
            fn += 'datatype={datatype}'.format(datatype)
            r = self._FMP_api_call(fn)
            return pd.read_csv(io.StringIO(r.content.decode('utf-8')))
        else:
            return self._FMP_api_call(fn).json() 
        
    def DJ_Constituents_Historical(self):
        fn = '/api/v3/historical/dowjones_constituent'

        return self._FMP_api_call(fn).json()
    
    def FX_Rate(self):
        fn = '/api/v3/fx?'

        return self._FMP_api_call(fn).json()

    def FX_Quotes(self):
        fn = '/api/v3/quotes/forex?'

        return self._FMP_api_call(fn).json()

    def FX_Rate_By_Pair(self, currency_pair):
        fn = '/api/v3/fx/{currency_pair}'.format(currency_pair)

        return self._FMP_api_call(fn).json()

    def FX_Quotes_By_Pair(self, currency_pair):
        fn = '/api/v3/quote/{currency_pair}'.format(currency_pair)

        return self._FMP_api_call(fn).json()
    
    def FX_Quotes_By_Pair_Historical(self, currency_pair, interval):
        fn = '/api/v3/historical-chart/{interval}/{currency_pair}'.format(interval, currency_pair)

        return self._FMP_api_call(fn).json()
    
    def Commodities_Prices_All(self):
        fn = '/api/v3/quotes/commodity'

        return self._FMP_api_call(fn).json()
    
    def Commodities_Prices_Historical(self, comm, interval):
        fn = '/api/v3/historical-chart/{interval}/{comm}'.format(interval, comm)

        return self._FMP_api_call(fn).json()       

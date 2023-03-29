from Utils.DataProvider import mysql_config, api_key_sql
import mysql.connector
import requests
import pandas as pd
import datetime

class AlphaVantage(object):

    def __init__(self) -> None:
        cnx = mysql.connector.connect(**mysql_config)
        cursor = cnx.cursor()
        cursor.execute(api_key_sql, [AlphaVantage.__name__])

        for _ in cursor:
            self.api_key = _[0]

        try: 
            url = 'https://www.alphavantage.co/documentation/'
            request = requests.get(url, timeout=5)
            print('AlphaVantage Connection Established')
        except:
            print("AlphaVantage Connection Failed")

    def _alphaVantage_api_call(self, fn, pandas_return=False,**kvarg):
        url = 'https://www.alphavantage.co/query?function={functionName}'.format(functionName=fn)

        for key in kvarg.keys():
            if kvarg[key] is None: continue
            url += '&{key}={value}'.format(key=key, value=kvarg[key])
        
        url += '&{key}={value}'.format(key='apikey', value=self.api_key)
        
        if pandas_return:
            with requests.Session() as s:
                download = s.get(url)
                decoded_content = download.content.decode('utf-8').splitlines()
                tmp_list = [row.split(',') for row in decoded_content]
                data = pd.DataFrame(tmp_list[1:], columns = tmp_list[0])
        else:
            r = requests.get(url)
            data = r.json()

        return data

######################################################################################################
#################################  Fundamental Data   ################################################
######################################################################################################

    def CompanyOverview(self, symbol):
        '''
        API Parameters
        ❚ Required: function
            The function of your choice. In this case, function=OVERVIEW
        ❚ Required: symbol
            The symbol of the token of your choice. For example: symbol=IBM.
        '''

        return self._alphaVantage_api_call('OVERVIEW', False, symbol=symbol)

    def IncomeStatement(self, symbol):
        '''
        API Parameters
        ❚ Required: function
            The function of your choice. In this case, function=INCOME_STATEMENT
        ❚ Required: symbol
            The symbol of the token of your choice. For example: symbol=IBM.
        '''

        return self._alphaVantage_api_call('INCOME_STATEMENT', pandas_return=False, symbol=symbol)

    def BalanceSheet(self, symbol):
        '''
        API Parameters
        ❚ Required: function
            The function of your choice. In this case, function=BALANCE_SHEET
        ❚ Required: symbol
            The symbol of the token of your choice. For example: symbol=IBM.
        '''

        return self._alphaVantage_api_call('BALANCE_SHEET', False, symbol=symbol)
    
    def CashflowStatement(self, symbol):
        '''
        API Parameters
        ❚ Required: function
            The function of your choice. In this case, function=CASH_FLOW
        ❚ Required: symbol
            The symbol of the token of your choice. For example: symbol=IBM.
        '''

        return self._alphaVantage_api_call('CASH_FLOW', False, symbol=symbol)
    
    def ReportedEPS_TimeSeries(self, symbol):
        '''
        ❚ Required: function
            The function of your choice. In this case, function=EARNINGS
        ❚ Required: symbol
            The symbol of the token of your choice. For example: symbol=IBM.
        '''
        
        return self._alphaVantage_api_call('EARNINGS', False, symbol=symbol)
    
    def ListingStatus(self, date=datetime.date.today(), state='active'):
        '''
        ❚ Required: function
            The API function of your choice. In this case, function=LISTING_STATUS
        ❚ Optional: date
            If no date is set, the API endpoint will return a list of active or delisted symbols as of the latest trading day. 
            If a date is set, the API endpoint will "travel back" in time and return a list of active or delisted symbols on that particular date in history. 
            Any YYYY-MM-DD date later than 2010-01-01 is supported. For example, date=2013-08-03
        ❚ Optional: state
            By default, state=active and the API will return a list of actively traded stocks and ETFs. Set state=delisted to query a list of delisted assets.
        '''
        
        return self._alphaVantage_api_call('LISTING_STATUS', True, date=date, state=state)

    def EarningsCalendar(self, symbol = None, horizon = '3month'):
        '''
        API Parameters
        ❚ Required: function
            The API function of your choice. In this case, function=EARNINGS_CALENDAR
        ❚ Optional: symbol
            By default, no symbol will be set for this API. 
            When no symbol is set, the API endpoint will return the full list of company earnings scheduled. 
            If a symbol is set, the API endpoint will return the expected earnings for that specific symbol. For example, symbol=IBM
        ❚ Optional: horizon
            By default, horizon=3month and the API will return a list of expected company earnings in the next 3 months. 
            You may set horizon=6month or horizon=12month to query the earnings scheduled for the next 6 months or 12 months, respectively.
        '''
        
        return self._alphaVantage_api_call('EARNINGS_CALENDAR', True, symbol=symbol, horizon=horizon)
    
    def IPOCalendar(self):
        '''
        API Parameters
        ❚ Required: function
            The API function of your choice. In this case, function=IPO_CALENDAR
        '''
        
        return self._alphaVantage_api_call('IPO_CALENDAR', True)

######################################################################################################
#################################   Core Stock APIs   ################################################
######################################################################################################

    def Time_Series_Intraday(self, symbol, interval, adjusted='true', outputsize='compact', datatype='json'):
        '''
        API Parameters
        ❚ Required: function
            The time series of your choice. In this case, function=TIME_SERIES_INTRADAY
        ❚ Required: symbol
            The name of the equity of your choice. For example: symbol=IBM
        ❚ Required: interval
            Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min
        ❚ Optional: adjusted
            By default, adjusted=true and the output time series is adjusted by historical split and dividend events. Set adjusted=false to query raw (as-traded) intraday values.
        ❚ Optional: outputsize
            By default, outputsize=compact. 
            Strings compact and full are accepted with the following specifications: 
            compact returns only the latest 100 data points in the intraday time series; full returns the full-length intraday time series. 
            The "compact" option is recommended if you would like to reduce the data size of each API call.
        ❚ Optional: datatype
            By default, datatype=json. 
            Strings json and csv are accepted with the following specifications: 
            json returns the intraday time series in JSON format; csv returns the time series as a CSV (comma separated value) file.
        '''
        
        return self._alphaVantage_api_call('TIME_SERIES_INTRADAY', datatype=='csv', symbol=symbol, interval=interval, adjusted=adjusted, outputsize=outputsize, datatype=datatype)

    def Time_Serires_Intraday_Extended(self, symbol, interval, slice='year1month1', adjusted='true'):
        '''
        ❚ Required: function
            The time series of your choice. In this case, function=TIME_SERIES_INTRADAY_EXTENDED
        ❚ Required: symbol
            The name of the equity of your choice. For example: symbol=IBM
        ❚ Required: interval
            Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min
        ❚ Required: slice
            Two years of minute-level intraday data contains over 2 million data points, which can take up to Gigabytes of memory. 
            To ensure optimal API response speed, the trailing 2 years of intraday data is evenly divided into 24 "slices" 
            - year1month1, year1month2, year1month3, ..., year1month11, year1month12, year2month1, year2month2, year2month3, ..., year2month11, year2month12. 
            Each slice is a 30-day window, with year1month1 being the most recent and year2month12 being the farthest from today. 
            By default, slice=year1month1.
        ❚ Optional: adjusted
            By default, adjusted=true and the output time series is adjusted by historical split and dividend events. Set adjusted=false to query raw (as-traded) intraday values.
        '''

        return self._alphaVantage_api_call('TIME_SERIES_INTRADAY_EXTENDED', True, symbol=symbol, interval=interval, slice=slice, adjusted=adjusted)

    def Time_Serires_Daily(self, symbol, outputsize='compact', datatype='json'):
        '''
        API Parameters
        ❚ Required: function
            The time series of your choice. In this case, function=TIME_SERIES_DAILY
        ❚ Required: symbol
            The name of the equity of your choice. For example: symbol=IBM
        ❚ Optional: outputsize
            By default, outputsize=compact. 
            Strings compact and full are accepted with the following specifications: 
            compact returns only the latest 100 data points; full returns the full-length time series of 20+ years of historical data. 
            The "compact" option is recommended if you would like to reduce the data size of each API call.
        ❚ Optional: datatype
            By default, datatype=json. 
            Strings json and csv are accepted with the following specifications: 
            json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file.
        '''

        return self._alphaVantage_api_call('TIME_SERIES_DAILY', datatype=='csv', symbol=symbol, outputsize=outputsize, datatype=datatype)

    def Time_Serires_Daily_Adjusted(self, symbol, outputsize='compact', datatype='json'):
        '''
        API Parameters
        ❚ Required: function
        The time series of your choice. In this case, function=TIME_SERIES_DAILY_ADJUSTED
        ❚ Required: symbol
        The name of the equity of your choice. For example: symbol=IBM
        ❚ Optional: outputsize
            By default, outputsize=compact. 
            Strings compact and full are accepted with the following specifications: 
            compact returns only the latest 100 data points; full returns the full-length time series of 20+ years of historical data. 
            The "compact" option is recommended if you would like to reduce the data size of each API call.
        ❚ Optional: datatype
            By default, datatype=json. 
            Strings json and csv are accepted with the following specifications: 
            json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file.
        '''

        return self._alphaVantage_api_call('TIME_SERIES_DAILY_ADJUSTED', datatype=='csv', symbol=symbol, outputsize=outputsize, datatype=datatype)

    def Time_Serires_Weekly(self, symbol, datatype='json'):
        '''
        API Parameters
        ❚ Required: function
            The time series of your choice. In this case, function=TIME_SERIES_WEEKLY
        ❚ Required: symbol
            The name of the equity of your choice. For example: symbol=IBM
        ❚ Optional: datatype
            By default, datatype=json. 
            Strings json and csv are accepted with the following specifications: 
            json returns the weekly time series in JSON format; csv returns the time series as a CSV (comma separated value) file.
        '''

        return self._alphaVantage_api_call('TIME_SERIES_WEEKLY', datatype=='csv', symbol=symbol, datatype=datatype)
    
    def Time_Serires_Weekly_Adjusted(self, symbol, datatype='json'):
        '''
        API Parameters
        ❚ Required: function
            The time series of your choice. In this case, function=TIME_SERIES_WEEKLY_ADJUSTED
        ❚ Required: symbol
            The name of the equity of your choice. For example: symbol=IBM
        ❚ Optional: datatype
            By default, datatype=json. 
            Strings json and csv are accepted with the following specifications: 
            json returns the weekly time series in JSON format; csv returns the time series as a CSV (comma separated value) file.
        '''

        return self._alphaVantage_api_call('TIME_SERIES_WEEKLY_ADJUSTED', datatype=='csv', symbol=symbol, datatype=datatype)

    def Time_Serires_Monthly(self, symbol, datatype='json'):
        '''
        API Parameters
        ❚ Required: function
            The time series of your choice. In this case, function=TIME_SERIES_MONTHLY
        ❚ Required: symbol
            The name of the equity of your choice. For example: symbol=IBM
        ❚ Optional: datatype
            By default, datatype=json. 
            Strings json and csv are accepted with the following specifications: 
            json returns the weekly time series in JSON format; csv returns the time series as a CSV (comma separated value) file.
        '''

        return self._alphaVantage_api_call('TIME_SERIES_MONTHLY', datatype=='csv', symbol=symbol, datatype=datatype)
    
    def Time_Serires_Monthly_Adjusted(self, symbol, datatype='json'):
        '''
        API Parameters
        ❚ Required: function
            The time series of your choice. In this case, function=TIME_SERIES_MONTHLY_ADJUSTED
        ❚ Required: symbol
            The name of the equity of your choice. For example: symbol=IBM
        ❚ Optional: datatype
            By default, datatype=json. 
            Strings json and csv are accepted with the following specifications: 
            json returns the weekly time series in JSON format; csv returns the time series as a CSV (comma separated value) file.
        '''

        return self._alphaVantage_api_call('TIME_SERIES_MONTHLY_ADJUSTED', datatype=='csv', symbol=symbol, datatype=datatype)
    
    def Quote_Endpoint(self, symbol, datatype='json'):
        '''
        API Parameters
        ❚ Required: function
            The API function of your choice.
        ❚ Required: symbol
            The symbol of the global token of your choice. For example: symbol=IBM.
        ❚ Optional: datatype
            By default, datatype=json. 
            Strings json and csv are accepted with the following specifications: 
            json returns the quote data in JSON format; csv returns the quote data as a CSV (comma separated value) file.
        '''

        return self._alphaVantage_api_call('GLOBAL_QUOTE', datatype=='csv', symbol=symbol, datatype=datatype)
    
    def Search_Endpoint(self, keywords, datatype='json'):
        '''
        API Parameters
        ❚ Required: function
            The API function of your choice. In this case, function=SYMBOL_SEARCH
        ❚ Required: keywords
            A text string of your choice. For example: keywords=microsoft.
        ❚ Optional: datatype
            By default, datatype=json. 
            Strings json and csv are accepted with the following specifications: 
            json returns the search results in JSON format; csv returns the search results as a CSV (comma separated value) file.
        '''

        return self._alphaVantage_api_call('SYMBOL_SEARCH', datatype=='csv', keywords=keywords, datatype=datatype)

    def Market_Status(self):
        '''
        API Parameters
        ❚ Required: function
            The API function of your choice. In this case, function=MARKET_STATUS
        '''

        return self._alphaVantage_api_call('MARKET_STATUS')    

######################################################################################################
#################################   Alpha Intelligence   #############################################
######################################################################################################

    def Market_News_Sentiment(self, tickers, topics, time_from, time_to, sort='LATEST', limit='50'):
        '''
        API Parameters
        ❚ Required: function
            The function of your choice. In this case, function=NEWS_SENTIMENT
        ❚ Optional: tickers
            The stock/crypto/forex symbols of your choice. For example: tickers=IBM will filter for articles that mention the IBM ticker; 
            tickers=COIN,CRYPTO:BTC,FOREX:USD will filter for articles that simultaneously mention Coinbase (COIN), Bitcoin (CRYPTO:BTC), 
            and US Dollar (FOREX:USD) in their content.
        ❚ Optional: topics
            The news topics of your choice. For example: topics=technology will filter for articles that write about the technology sector; 
            topics=technology,ipo will filter for articles that simultaneously cover technology and IPO in their content. 
            Below is the full list of supported topics:
                Blockchain: blockchain
                Earnings: earnings
                IPO: ipo
                Mergers & Acquisitions: mergers_and_acquisitions
                Financial Markets: financial_markets
                Economy - Fiscal Policy (e.g., tax reform, government spending): economy_fiscal
                Economy - Monetary Policy (e.g., interest rates, inflation): economy_monetary
                Economy - Macro/Overall: economy_macro
                Energy & Transportation: energy_transportation
                Finance: finance
                Life Sciences: life_sciences
                Manufacturing: manufacturing
                Real Estate & Construction: real_estate
                Retail & Wholesale: retail_wholesale
                Technology: technology
        ❚ Optional: time_from and time_to
           The time range of the news articles you are targeting, in YYYYMMDDTHHMM format. 
           For example: time_from=20220410T0130. 
           If time_from is specified but time_to is missing, the API will return articles published between the time_from value and the current time.
        ❚ Optional: sort
            By default, sort=LATEST and the API will return the latest articles first. You can also set sort=EARLIEST or sort=RELEVANCE based on your use case.
        ❚ Optional: limit
            By default, limit=50 and the API will return up to 50 matching results. 
            You can also set limit=200 to output up to 200 results. 
            If you are looking for an even higher output limit, please contact support@alphavantage.co to have your limit boosted.
        '''

        return self._alphaVantage_api_call('NEWS_SENTIMENT', tickers=tickers, topics=topics, time_from=time_from, time_to=time_to, sort=sort, limit=limit)
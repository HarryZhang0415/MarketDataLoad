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
            print('AlphaVantage Connection Test Finished')
        except:
            print("Cannot Find Connection to AlphaVantage")

    def CompanyOverview(self, symbol):
        '''
        API Parameters
        Required: function
        The function of your choice. In this case, function=OVERVIEW
        Required: symbol
        The symbol of the token of your choice. For example: symbol=IBM.
        Required: apikey
        '''
        url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol=%s&apikey=%s' % (symbol, self.api_key)
        r = requests.get(url)
        data = r.json()

        return data

    def IncomeStatement(self, symbol):
        '''
        API Parameters
        Required: function
        The function of your choice. In this case, function=INCOME_STATEMENT
        Required: symbol
        The symbol of the token of your choice. For example: symbol=IBM.
        Required: apikey
        '''
        url = 'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=%s&apikey=%s' % (symbol, self.api_key)
        r = requests.get(url)
        data = r.json()

        return data

    def BalanceSheet(self, symbol):
        '''
        API Parameters
        Required: function
        The function of your choice. In this case, function=BALANCE_SHEET
        Required: symbol
        The symbol of the token of your choice. For example: symbol=IBM.
        Required: apikey
        '''
        url = 'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=%s&apikey=%s' % (symbol, self.api_key)
        r = requests.get(url)
        data = r.json()

        return data
    
    def CashflowStatement(self, symbol):
        '''
        API Parameters
        Required: function
        The function of your choice. In this case, function=CASH_FLOW
        Required: symbol
        The symbol of the token of your choice. For example: symbol=IBM.
        Required: apikey
        '''
        url = 'https://www.alphavantage.co/query?function=CASH_FLOW&symbol=%s&apikey=%s' % (symbol, self.api_key)
        r = requests.get(url)
        data = r.json()

        return data
    
    def ReportedEPS_TimeSeries(self, symbol):
        '''
        Required: function
        The function of your choice. In this case, function=EARNINGS
        Required: symbol
        The symbol of the token of your choice. For example: symbol=IBM.
        Required: apikey
        '''
        url = 'https://www.alphavantage.co/query?function=EARNINGS&symbol=%s&apikey=%s' % (symbol, self.api_key)
        r = requests.get(url)
        data = r.json()

        return data
    
    def ListingStatus(self, date=datetime.date.today(), state='active'):
        '''
        Required: function
        The API function of your choice. In this case, function=LISTING_STATUS
        Optional: date
        If no date is set, the API endpoint will return a list of active or delisted symbols as of the latest trading day. If a date is set, the API endpoint will "travel back" in time and return a list of active or delisted symbols on that particular date in history. Any YYYY-MM-DD date later than 2010-01-01 is supported. For example, date=2013-08-03
        Optional: state
        By default, state=active and the API will return a list of actively traded stocks and ETFs. Set state=delisted to query a list of delisted assets.
        Required: apikey
        '''
        CSV_URL = 'https://www.alphavantage.co/query?function=LISTING_STATUS'
        CSV_URL += '&date=%s' % date
        CSV_URL += '&state=%s' % state
        CSV_URL += '&apikey=%s' % self.api_key
        with requests.Session() as s:
            download = s.get(CSV_URL)
            decoded_content = download.content.decode('utf-8').splitlines()
            tmp_list = [row.split(',') for row in decoded_content]
            data = pd.DataFrame(tmp_list[1:], columns = tmp_list[0])
        
        return data.set_index('symbol')

    def EarningsCalendar(self, symbol = None, horizon = '3month'):
        '''
        API Parameters
        Required: function
        The API function of your choice. In this case, function=EARNINGS_CALENDAR
        Optional: symbol
        By default, no symbol will be set for this API. When no symbol is set, the API endpoint will return the full list of company earnings scheduled. If a symbol is set, the API endpoint will return the expected earnings for that specific symbol. For example, symbol=IBM
        Optional: horizon
        By default, horizon=3month and the API will return a list of expected company earnings in the next 3 months. You may set horizon=6month or horizon=12month to query the earnings scheduled for the next 6 months or 12 months, respectively.
        Required: apikey
        '''
        CSV_URL = 'https://www.alphavantage.co/query?function=EARNINGS_CALENDAR'
        
        if symbol is not None:
            CSV_URL += '&symbol=%s' % symbol

        CSV_URL += '&horizon=%s' % horizon
        CSV_URL += '&apikey=%s' % self.api_key
        with requests.Session() as s:
            download = s.get(CSV_URL)
            decoded_content = download.content.decode('utf-8').splitlines()
            tmp_list = [row.split(',') for row in decoded_content]
            data = pd.DataFrame(tmp_list[1:], columns = tmp_list[0])
        
        return data.set_index('symbol')
    
    def IPOCalendar(self):
        '''
        API Parameters
        Required: function
        The API function of your choice. In this case, function=IPO_CALENDAR
        Required: apikey
        '''
        CSV_URL = 'https://www.alphavantage.co/query?function=IPO_CALENDAR'
        CSV_URL += '&apikey=%s' % self.api_key
        with requests.Session() as s:
            download = s.get(CSV_URL)
            decoded_content = download.content.decode('utf-8').splitlines()
            tmp_list = [row.split(',') for row in decoded_content]
            data = pd.DataFrame(tmp_list[1:], columns = tmp_list[0])
        
        return data.set_index('symbol')





test = AlphaVantage()
df = test.IPOCalendar()

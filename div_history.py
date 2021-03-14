import requests
import boto3
import csv
import time

def upload_ticker(my_file, ticker):
    s3_client = boto3.client('s3')
    s3_file = f'stocks/{ticker}.csv'
    s3_client.upload_file(my_file, 'divdata', s3_file)

def get_data(filename, ticker):
    period2= int(time.time())
    dividend_url = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1=1&period2={period2}&interval=1d&events=div&includeAdjustedClose=true'
    r = requests.get(dividend_url, allow_redirects=True)
    open(filename, 'wb').write(r.content)

def convert_row_to_data(html):
    columns = html.findAll('td')
    data = {}
    data['Date'] = columns[0].text
    data['Amount per Share'] = columns[1].text
    data['Note'] = columns[2].text
    return data

def lambda_handler(event, context):
    ticker = event['queryStringParameters']['Ticker']
    filename = f'/tmp/{ticker}.csv'
    get_data(filename, ticker)
    upload_ticker(filename, ticker)

if __name__ == "__main__":
    ticker = input('Enter Ticker: ')
    filename = f'{ticker}.csv'
    get_data(filename, ticker)
    upload_ticker(filename, ticker)


import os
from dotenv import load_dotenv
import httpx
import calendar


load_dotenv()

EXCHANGE_RATE_API_VERSION = os.getenv("EXCHANGE_RATE_API_VERSION")
EXCHANGE_RATE_API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
EXCHANGE_RATE_API_URL = 'https://'+''+EXCHANGE_RATE_API_VERSION+'.exchangerate-api.com/'+EXCHANGE_RATE_API_VERSION+'/'+EXCHANGE_RATE_API_KEY+'/latest/USD'
print(EXCHANGE_RATE_API_URL)

async def get_all_conversion_rates():
    async with httpx.AsyncClient() as client:
        response = await client.get(EXCHANGE_RATE_API_URL)
        if response.status_code == 200:
            return response.json()["conversion_rates"]
        else:
            raise Exception(f"Failed to retrieve data, status code: {response.status_code}")

async def get_exchange_rate(currency: str):
    if(currency == 'USD'):
        return 1
    data = await get_all_conversion_rates()
    conversion_rate = data[currency]
    if(conversion_rate is None):
        raise ValueError(f"Invalid currency code: {currency}")
    return conversion_rate

async def get_converted_amount_to_usd(amount, currency):
    # to reduce API calls, if the currency is USD, return the amount as is
    if(currency == 'USD'):
        return amount
    data = await get_all_conversion_rates()
    conversion_rate = data[currency]
    if(conversion_rate is None):
        raise ValueError(f"Invalid currency code: {currency}")
    return amount / conversion_rate

async def get_amount_in_currency_from_usd(amount, currency):
    # to reduce API calls, if the currency is USD, return the amount as is
    if(currency == 'USD'):
        return amount
    data = await get_all_conversion_rates()
    conversion_rate = data[currency]
    if(conversion_rate is None):
        raise ValueError(f"Invalid currency code: {currency}")
    return amount * conversion_rate

def get_month_name(month_number):
    return calendar.month_name[month_number]

# to be done in the future
# def hash_password(password: str):
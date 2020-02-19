import requests
from datetime import datetime

ENDPOINT = 'http://api.openweathermap.org/data/2.5/forecast'
PARAMETERS = '?q=minneapolis,us&units=imperial&APPID=09110e603c1d5c272f94f64305c09436'


def run():
    response = requests.get(f'{ENDPOINT}{PARAMETERS}')
    forecast_list = response.json()['list']
    daily_forecasts = get_daily_forecasts(forecast_list)
    daily_averages = get_daily_averages(daily_forecasts)
    results = get_contact_method(daily_averages)
    print_formatted_results(results)


# The API returns a list of forecasts for every 3 hours over the next 5 day period.
# This method returns a list of lists representing each forecast for each day.
def get_daily_forecasts(forecast_list):
    daily_forecasts = [[]]
    current_index = 0
    current_date = datetime.utcfromtimestamp(forecast_list[0]['dt'])
    for item in forecast_list:
        dt = datetime.utcfromtimestamp(item['dt'])
        if dt.date() <= current_date.date():
            daily_forecasts[current_index].append(item)
        else:
            current_index += 1
            current_date = dt
            daily_forecasts.append(list())
            daily_forecasts[current_index].append(item)

    return daily_forecasts


# This function returns a list of dictionary objects containing attributes relevant to our engagement rules.
def get_daily_averages(daily_forecasts):
    daily_averages = []
    for daily in daily_forecasts:
        avg_temp = sum(forecast['main']['temp'] for forecast in daily)/len(daily)
        daily_averages.append(dict(date=datetime.utcfromtimestamp(daily[0]['dt']).date(),
                                   avg_temp=avg_temp,
                                   is_rainy=is_day_rainy(daily),
                                   is_sunny=is_day_sunny(daily)))
    return daily_averages


# A day is classified as rainy if any forecast contains rain.
def is_day_rainy(daily):
    for forecast in daily:
        if 'rain' in forecast:
            return True
    return False


# A day is classified as sunny if cloud coverage is never above 10%.
def is_day_sunny(daily):
    for forecast in daily:
        if forecast['clouds']['all'] >= 10:
            return False
    return True


# Rules for determining contact method:
# 1. The best time to engage a customer via a text message is when it is
#   sunny and warmer than 75 degrees Fahrenheit.
# 2. The best time to engage a customer via email is when it is between 55 and 75 degrees Fahrenheit.
# 3. The best time to engage a customer via a phone call is when it is less than 55 degrees or when it
#   is raining.
#
# These rules create three known uncertain cases:
# 1. Temperature is above 75 but NOT sunny? (Text?)
#         Chosen solution: Text
# 2. Temperature is above 75 but rainy? (Text or call?)
#         Chosen solution: call
# 3. Temperature is between 55 and 75 but rainy? (Email or call?)
#         Chosen solution: call
#
def get_contact_method(daily_averages):
    results = []
    for daily in daily_averages:
        if daily['is_rainy'] or daily['avg_temp'] < 55:
            results.append(dict(date=daily['date'], method='call'))
            continue
        if daily['avg_temp'] <= 75:
            results.append(dict(date=daily['date'], method='email'))
            continue
        results.append(dict(date=daily['date'], method='text'))

    return results


def print_formatted_results(results):
    for result in results:
        print(f'{result["date"]} {result["method"]}')

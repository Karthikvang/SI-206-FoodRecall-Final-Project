import requests
import sqlite3
import datetime


openweather_key = '6cebbdc5722158ef937fa0f74650b54b'
DAY_INCREMENT = 86400 # Number of seconds in a day, required for incrementing days


def get_geocode(city_str):
    limit = 1
    url = f'''http://api.openweathermap.org/geo/1.0/direct?q={city_str}, MI, USA&limit={limit}&appid={openweather_key}'''
    geocode = requests.get(url).json()

    latitude = geocode[0]['lat']
    longitude = geocode[0]['lon']

    return (latitude, longitude)


def get_may_data(lat, lon):
    start = 1714536000 # May 1 2024 12:00AM
    end = 1714622400 # May 2 2024 12:00AM

    end_of_month = 1717214400 # June 1 2024

    may_lst = []
    
    while start < end_of_month:

        # Call data for noon of every day in may
        url = f'https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&appid={openweather_key}&start={str(start)}&end={str(end)}&units=imperial'
        response = requests.get(url)
        response = response.json()['list'][12]

        # Change date from unix timestamp into regular calendar date
        timestamp = response['dt']
        date = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
        response['dt'] = str(date.date())

        # Move on to the next day
        start += DAY_INCREMENT
        end += DAY_INCREMENT

        may_lst.append(response)

    return may_lst


def get_july_data(lat,lon):
    start = 1719806400 # July 1 2024 12:00AM
    end = 1719892800 # July 2 2024 12:00AM

    end_of_month = 1722484800 # August 1 2024

    july_dict = []
    
    while int(start) < end_of_month:

        # Call data for noon of every day in may
        url = f'https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&appid={openweather_key}&start={str(start)}&end={str(end)}&units=imperial'
        response = requests.get(url)
        response = response.json()['list'][12]

        # Change date from unix timestamp into regular calendar date
        timestamp = response['dt']
        date = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
        response['dt'] = str(date.date())

        # Move on to the next day
        start += DAY_INCREMENT
        end += DAY_INCREMENT

        july_dict.append(response)

    return july_dict
    

def get_september_data(lat,lon):
    start = 1725163200 # September 1 2024 12:00AM
    end = 1725249600 # September 2 2024 12:00AM
    
    end_of_month = 1727755200 # October 1 2024

    september_lst = []

    while int(start) < end_of_month:

        # Call data for noon of every day in may
        url = f'https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&appid={openweather_key}&start={str(start)}&end={str(end)}&units=imperial'
        response = requests.get(url)
        response = response.json()['list'][9]

        # Change date from unix timestamp into regular calendar date
        timestamp = response['dt']
        date = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
        response['dt'] = str(date.date())

        # Move on to the next day
        start += DAY_INCREMENT
        end += DAY_INCREMENT

        september_lst.append(response)


    return september_lst


def get_january_data(lat,lon):
    start = 1735707600 # January 1 2025 12:00AM
    end = 1735794000 # January 2 2025 12:00AM

    end_of_month = 1738386000 # February 1 2025

    january_lst = []
    
    while int(start) < end_of_month:

        # Call data for noon of every day in may
        url = f'https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&appid={openweather_key}&start={str(start)}&end={str(end)}&units=imperial'
        response = requests.get(url)
        response = response.json()['list'][9]

        # Change date from unix timestamp into regular calendar date
        timestamp = response['dt']
        date = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
        response['dt'] = str(date.date())

        # Move on to the next day
        start += DAY_INCREMENT
        end += DAY_INCREMENT
        january_lst.append(response)

    return january_lst


def create_db():
    conn = sqlite3.connect('A2N.db')
    cur = conn.cursor()

    # City (cannot be primary key)
    # Date ()
    # Time (time cannot be primary key)
    # Temperature 

    cur.execute("""CREATE TABLE IF NOT EXISTS weather (
                
                
                )""")


def insert_seasons (season, cur, conn, limit = 25):
    
    for city in season:
        for item in season[city]['list']:
            time = item[city]['dt']
            print(time)
            temp = item['main']['temp']


def main():

    # Get coordinates to help API locate city
    aa_geocode = get_geocode('Ann Arbor')
    dt_geocode = get_geocode('Detroit')
    pc_geocode = get_geocode('Pontiac')

    # Organize returned data into summer & winter dictionaries
    may = get_may_data(aa_geocode[0], aa_geocode[1])
    print(f'MAY\n{may}')
    jan = get_january_data(aa_geocode[0], aa_geocode[1])
    print(f'JAN\n{jan}')
    sept = get_september_data(aa_geocode[0], aa_geocode[1])
    print(f'SEPT\n{sept}')
    july = get_july_data(aa_geocode[0], aa_geocode[1])
    print(f'JULY\n{july}')
    

    # insert_seasons(summer_dict, cur, conn)

   

if __name__ == "__main__":
    main()

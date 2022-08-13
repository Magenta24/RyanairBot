from collections import namedtuple

Airport = namedtuple('Airport', ['city', 'country', 'IATA_code'])
Airports = {
    'Krakow': Airport('Krakow', 'Polska', 'KRK'),
    'Wroclaw': Airport('Wroclaw', 'Polska', 'WRO'),
    'Katowice': Airport('Katowice', 'Polska', 'KTW'),
    'Poznan': Airport('Poznan', 'Polska', 'POZ'),
    'Gdansk': Airport('Gdansk', 'Polska', 'GDN'),
    'Warszawa-Modlin': Airport('Warszawa-Modlin', 'Polska', 'WMI'),
}


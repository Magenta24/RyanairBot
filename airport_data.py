from collections import namedtuple

Airport = namedtuple('Airport', ['city', 'country', 'IATA_code', 'currency'])
Airports = {
    'Krakow': Airport('Krakow', 'Polska', 'KRK', 'PLN'),
    'Wroclaw': Airport('Wroclaw', 'Polska', 'WRO', 'PLN'),
    'Katowice': Airport('Katowice', 'Polska', 'KTW', 'PLN'),
    'Poznan': Airport('Poznan', 'Polska', 'POZ', 'PLN'),
    'Gdansk': Airport('Gdansk', 'Polska', 'GDN', 'PLN'),
    'Warszawa-Modlin': Airport('Warszawa-Modlin', 'Polska', 'WMI', 'PLN'),
    'Bratyslawa': Airport('Bratislava', 'Słowacja', 'BTS', 'EUR'),
    'Leeds': Airport('Leeds/Bradford', 'Wielka Brytania', 'LBA', 'GBP')
}


from collections import namedtuple

Airport = namedtuple('Airport', ['city', 'country', 'IATA_code', 'currency'])
Connection = namedtuple('Connection', ['departure_port', 'destination_ports'])

Airports = {
    # Poland
    'Krakow': Airport('Krakow', 'Polska', 'KRK', 'PLN'),
    'Wroclaw': Airport('Wroclaw', 'Polska', 'WRO', 'PLN'),
    'Katowice': Airport('Katowice', 'Polska', 'KTW', 'PLN'),
    'Poznan': Airport('Poznan', 'Polska', 'POZ', 'PLN'),
    'Gdansk': Airport('Gdansk', 'Polska', 'GDN', 'PLN'),
    'Warszawa-Modlin': Airport('Warszawa-Modlin', 'Polska', 'WMI', 'PLN'),
    # Slovakia
    'Bratyslawa': Airport('Bratislava', 'Słowacja', 'BTS', 'EUR'),
    # Czech Republic
    # Germany
    'Berlin': Airport('Berlin Brandenburg', 'Niemcy', 'BER', 'EUR'),
    'Dortmund': Airport('Dortmund', 'Niemcy', 'DTM', 'EUR'),
    'Dusseldorf': Airport('Dusseldorf-Weeze', 'Niemcy', 'NRN', 'EUR'),
    'Lipsk': Airport('Lipsk/Halle', 'Niemcy', 'LEJ', 'EUR'),
    'Hamburg': Airport('Hamburg', 'Niemcy', 'HAM', 'EUR'),
    'Dresden': Airport('Dresden', 'Niemcy', 'DRS', 'EUR'),
    'Frankfurt': Airport('Frankfurt-Hahn', 'Niemcy', 'HHN', 'EUR'),
    # Spain
    # Portugal
    # Great Britain
    'Leeds': Airport('Leeds/Bradford', 'Wielka Brytania', 'LBA', 'GBP'),
    'Birmingham': Airport('Birmingham', 'Wielka Brytania', 'BHX', 'GBP'),
    'East Midlands': Airport('East Midlands', 'Wielka Brytania', 'EMA', 'GBP'),
    'Manchester': Airport('Manchester', 'Wielka Brytania', 'MAN', 'GBP'),
    'Liverpool': Airport('Liverpool', 'Wielka Brytania', 'LPL', 'GBP'),
    'Cardiff': Airport('Cardiff', 'Wielka Brytania', 'CWL', 'GBP'),
    'Bristol': Airport('Bristol', 'Wielka Brytania', 'BRS', 'GBP')
}

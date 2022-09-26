from collections import namedtuple

Airport = namedtuple('Airport', ['city', 'country', 'IATA_code', 'currency', 'connections'])
Connection = namedtuple('Connection', ['departure_port', 'destination_ports'])


Airports = {

    # Poland
    'Krakow': Airport('Krakow', 'Polska', 'KRK', 'PLN', ('Wieden', 'Bruksela-Charleroi', 'Prague', 'Leeds', 'Manchester', 'Goteborg')),
    'Wroclaw': Airport('Wroclaw', 'Polska', 'WRO', 'PLN', ('Krakow')),
    'Katowice': Airport('Katowice', 'Polska', 'KTW', 'PLN', ('Krakow')),
    'Poznan': Airport('Poznan', 'Polska', 'POZ', 'PLN', ('Krakow')),
    'Gdansk': Airport('Gdansk', 'Polska', 'GDN', 'PLN', ('Krakow')),
    'Warszawa-Modlin': Airport('Warszawa-Modlin', 'Polska', 'WMI', 'PLN', ('Krakow')),
    'Szczecin': Airport('Szczecin', 'Polska', 'SZZ', 'PLN', ('Krakow')),
    'Lodz': Airport('Łódż', 'Polska', 'LCJ', 'PLN', ('Krakow')),
    'Bydgoszcz': Airport('Bydgoszcz', 'Polska', 'BZG', 'PLN', ('Krakow')),

    # Austria
    'Wieden': Airport('Wiedeń', 'Austria', 'WMI', 'EUR', ('Krakow')),
    'Salzburg': Airport('Salzburg', 'Austria', 'WMI', 'EUR', ('Krakow')),
    'Klagenfurt': Airport('Klagenfurt', 'Austria', 'WMI', 'EUR', ('Krakow')),

    # Slovakia
    'Bratyslawa': Airport('Bratislava', 'Słowacja', 'BTS', 'EUR', ('Krakow')),
    'Kosice': Airport('Kosice', 'Słowacja', 'KSC', 'EUR', ('Krakow')),

    # Czech Republic
    'Brno': Airport('Brno', 'Czechy', 'BRQ', 'CZK', ('Krakow')),
    'Ostrava': Airport('Ostrava', 'Czechy', 'OSR', 'CZK', ('Krakow')),
    'Pardubice': Airport('Pardubice', 'Czechy', 'PED', 'CZK', ('Krakow')),
    'Praga': Airport('Prague', 'Czechy', 'PRG', 'CZK', ('Krakow')),

    # Germany
    'Berlin': Airport('Berlin Brandenburg', 'Niemcy', 'BER', 'EUR', ('Krakow')),
    'Dortmund': Airport('Dortmund', 'Niemcy', 'DTM', 'EUR', ('Krakow')),
    'Dusseldorf': Airport('Dusseldorf-Weeze', 'Niemcy', 'NRN', 'EUR', ('Krakow')),
    'Lipsk': Airport('Lipsk/Halle', 'Niemcy', 'LEJ', 'EUR', ('Krakow')),
    'Hamburg': Airport('Hamburg', 'Niemcy', 'HAM', 'EUR', ('Krakow')),
    'Dresden': Airport('Dresden', 'Niemcy', 'DRS', 'EUR', ('Krakow')),
    'Frankfurt': Airport('Frankfurt-Hahn', 'Niemcy', 'HHN', 'EUR', ('Krakow')),

    # Spain
    'Alicante': Airport('Alicante', 'Hiszpania', 'ALC', 'EUR', ('Krakow')),
    'Barcelona-El Prat': Airport('Barcelona-El Prat', 'Hiszpania', 'BCN', 'EUR', ('Krakow')),
    'Barcelona-Reus': Airport('Barcelona-Reus', 'Hiszpania', 'REU', 'EUR', ('Krakow')),
    'Barcelona-Girona': Airport('Barcelona-Girona', 'Hiszpania', 'GRO', 'EUR', ('Krakow')),
    'Ibiza': Airport('Ibiza', 'Hiszpania', 'IBZ', 'EUR', ('Krakow')),
    'Gran Canaria': Airport('Gran Canaria(Las Palmas)', 'Hiszpania', 'LPA', 'EUR', ('Krakow')),
    'La Palma': Airport('La Palma', 'Hiszpania', 'SPC', 'EUR', ('Krakow')),
    'Madryt': Airport('Madryt', 'Hiszpania', 'MAD', 'EUR', ('Krakow')),
    'Malaga': Airport('Malaga', 'Hiszpania', 'AGP', 'EUR', ('Krakow')),
    'Sewilla': Airport('Sewilla', 'Hiszpania', 'SVQ', 'EUR', ('Krakow')),

    # Portugal
    'Lizbona': Airport('Lisbon', 'Portugalia', 'LIS', 'EUR', ('Krakow')),
    'Faro': Airport('Faro', 'Portugalia', 'FAO', 'EUR', ('Krakow')),
    'Porto': Airport('Porto', 'Portugalia', 'OPO', 'EUR', ('Krakow')),

    # Italy
    'Bolonia': Airport('Bolonia', 'Włochy', 'BLQ', 'EUR', ('Krakow')),
    'Mediolan-Bergamo': Airport('Mediolan-Bergamo', 'Włochy', 'BGM', 'EUR', ('Krakow')),
    'Mediolan-Malpensa': Airport('Mediolan-Malpensa', 'Włochy', 'MXP', 'EUR', ('Krakow')),
    'Neapol': Airport('Neapol', 'Włochy', 'NAP', 'EUR', ('Krakow')),
    'Palermo': Airport('Palermo', 'Włochy', 'PMO', 'EUR', ('Krakow')),
    'Rimini': Airport('Rimini', 'Włochy', 'RMI', 'EUR', ('Krakow')),
    'Rzym-Ciampino': Airport('Rzym-Ciampino', 'Włochy', 'CIA', 'EUR', ('Krakow')),
    'Rzym-Fiumcino': Airport('Rzym-Fiumcino', 'Włochy', 'FCO', 'EUR', ('Krakow')),
    'Triest': Airport('Triest', 'Włochy', 'TRS', 'EUR', ('Krakow')),
    'Turyn': Airport('Turyn', 'Włochy', 'TRN', 'EUR', ('Krakow')),
    'Wenecja M.Polo': Airport('Wenecja M.Polo', 'Włochy', 'VCE', 'EUR', ('Krakow')),
    'Wenecja-Treviso': Airport('Wenecja-Treviso', 'Włochy', 'TSF', 'EUR', ('Krakow')),
    'Werona': Airport('Werona', 'Włochy', 'VRN', 'EUR', ('Krakow')),

    # Great Britain
    'Leeds': Airport('Leeds/Bradford', 'Wielka Brytania', 'LBA', 'GBP', ('Krakow')),
    'Birmingham': Airport('Birmingham', 'Wielka Brytania', 'BHX', 'GBP', ('Krakow')),
    'East Midlands': Airport('East Midlands', 'Wielka Brytania', 'EMA', 'GBP', ('Krakow')),
    'Manchester': Airport('Manchester', 'Wielka Brytania', 'MAN', 'GBP', ('Krakow')),
    'Liverpool': Airport('Liverpool', 'Wielka Brytania', 'LPL', 'GBP', ('Krakow')),
    'Cardiff': Airport('Cardiff', 'Wielka Brytania', 'CWL', 'GBP', ('Krakow')),

    # Irlandia
    'Dublin': Airport('Dublin', 'Irlandia', 'DUB', 'EUR', ('Krakow')),
    'Cork': Airport('Cork', 'Irlandia', 'ORK', 'EUR', ('Krakow')),
    'Kerry': Airport('Kerry', 'Irlandia', 'KIR', 'EUR', ('Krakow')),
    'Shannon': Airport('Shannon', 'Irlandia', 'SNN', 'EUR', ('Krakow')),
    'Knock': Airport('Dublin', 'Irlandia', 'NOC', 'EUR', ('Krakow')),


    # Denmark
    'Aalborg': Airport('Aalborg', 'Dania', 'AAL', 'DKK', ('Krakow')),
    'Aarhus': Airport('Aarhus', 'Dania', 'AAR', 'DKK', ('Krakow')),
    'Billund': Airport('Billund', 'Dania', 'BLL', 'DKK', ('Krakow')),
    'Copenhagen': Airport('Kopenhaga', 'Dania', 'CPH', 'DKK', ('Krakow')),
    'Esbjerg': Airport('Esbjerg', 'Dania', 'EBJ', 'DKK', ('Krakow')),

    # Finland
    'Helsinki': Airport('Helsinki', 'Finlandia', 'HEL', 'EUR', ('Krakow')),
    'Lappeenranta': Airport('Lappeenranta', 'Finlandia', 'LPP', 'EUR', ('Krakow')),
    'Rovaniemi': Airport('Laponia Rovaniemi', 'Finlandia', 'RVN', 'EUR', ('Krakow')),
    'Tampere': Airport('Tampere', 'Finlandia', 'TMP', 'EUR', ('Krakow')),

    # Netherlands
    'Amsterdam': Airport('Amsterdam', 'Holandia', 'AMS', 'EUR', ('Krakow')),
    'Eindhoven': Airport('Eindhoven', 'Holandia', 'EIN', 'EUR', ('Krakow')),
    'Maastricht': Airport('Maastricht', 'Holandia', 'MST', 'EUR', ('Krakow')),

    # Sweden
    'Goteborg': Airport('Goteborg-Landvetter', 'Szwecja', 'GOT', 'SEK', ('Krakow')),
    'Lulea': Airport('Lulea', 'Szwecja', 'LLA', 'SEK', ('Krakow')),
    'Malmo': Airport('Goteborg-Landvetter', 'Szwecja', 'MMX', 'SEK', ('Krakow')),
    'Orebro': Airport('Goteborg-Landvetter', 'Szwecja', 'ORB', 'SEK', ('Krakow')),
    'Skelleftea': Airport('Goteborg-Landvetter', 'Szwecja', 'SFT', 'SEK', ('Krakow')),
    'Stockholm-Alranda': Airport('Goteborg-Landvetter', 'Szwecja', 'ARN', 'SEK', ('Krakow')),
    'Stockholm-Vasteras': Airport('Goteborg-Landvetter', 'Szwecja', 'VST', 'SEK', ('Krakow')),
    'Vaxjo-Smaland': Airport('Goteborg-Landvetter', 'Szwecja', 'VXO', 'SEK', ('Krakow')),
    'Visby-Gotland': Airport('Goteborg-Landvetter', 'Szwecja', 'VBY', 'SEK', ('Krakow')),

    # Norway
    'Haugesund': Airport('Haugesund', 'Norwegia', 'EBJ', 'NOK', ('Krakow')),
    'Oslo': Airport('Oslo', 'Norwegia', 'OSL', 'NOK', ('Krakow')),
    'Oslo-Torp': Airport('Oslo-Torp', 'Norwegia', 'TRF', 'NOK', ('Krakow')),

    # Belgium
    'Bruksela-Zaventem': Airport('Bruksela-Zaventem', 'Belgia', 'BRU', 'EUR', ('Krakow')),
    'Bruksela-Charleroi': Airport('Bruksela-Charleroi', 'Belgia', 'CRL', 'EUR', ('Krakow')),


}

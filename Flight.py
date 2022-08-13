import datetime
from airport_data import Airports

class Flight:

    # class attributes with default values
    __departure_country = None
    __departure_city = None
    __depart_port_IATA_code = None
    __destination_country = 'Wielka Brytania'
    __destination_city = 'Leeds'
    __dest_port_IATA_code = 'LBA'
    __date = None
    __price = -1

    # def __init__(self):
    #     pass
    #
    def __init__(self, depart_city, dest_city):
        self.__departure_city = depart_city
        self.__destination_city = dest_city
        self.__depart_IATA_code = Airports[depart_city].IATA_code

    def setPrice(self, price):
        self.__price = price

    def setDate(self, date):
        self.__date = date

    def getDepartureCity(self):
        return self.__departure_city

    def getDepartureCountry(self):
        return self.__departure_country

    def getDeparturePortIATACode(self):
        return self.__depart_IATA_code

    def getDestinationCity(self):
        return self.__destination_city

    def getDestinationCountry(self):
        return self.__destination_country

    def getDestinationPortIATACode(self):
        return self.__dest_port_IATA_code

    def getFlightDate(self):
        return self.__date

    def getPrice(self):
        return self.__price

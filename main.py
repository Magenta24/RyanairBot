import threading
import time
from RyanairBot import RyanairBot


departure_cities = ('Krakow', 'Wroclaw', 'Poznan')

bot_krk = RyanairBot('Chrome', 'Krakow', 'Leeds')
botek_poz = RyanairBot('Chrome', 'Poznan', 'Leeds')
botek_wro = RyanairBot('Chrome', 'Wroclaw', 'Leeds')

t_krk = threading.Thread(target=bot_krk.run())
t_poz = threading.Thread(target=botek_poz.run())
t_wro = threading.Thread(target=botek_wro.run())

t_krk.start()
t_wro.start()
t_poz.start()


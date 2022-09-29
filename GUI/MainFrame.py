from tkinter import ttk
import tkinter as tk
from tkcalendar import Calendar


class MainFrame(ttk.Frame):

    def __init__(self, container, row, function):
        super().__init__(container)
        self.grid(row=row, sticky=tk.EW, padx=70, ipady=50)
        self.__composeWidgets(function)

    def __composeWidgets(self, function):
        # departure city capture (parent - main_frame)
        depart_city_frame = ttk.LabelFrame(self, text='Choose departure city')
        depart_city_frame.grid(row=0, column=0, pady=30)

        depart_city = tk.StringVar()
        depart_city_widget = ttk.Entry(depart_city_frame, textvariable=depart_city)
        depart_city_widget.grid(row=0, column=0)

        # destination city capture
        dest_city_frame = ttk.LabelFrame(self, text='Choose departure city')
        dest_city_frame.grid(row=0, column=1, pady=30)

        dest_city = tk.StringVar()
        dest_city_widget = ttk.Entry(dest_city_frame, textvariable=dest_city)
        dest_city_widget.grid(row=0, column=1)

        # start search date
        choose_start_date_frame = ttk.LabelFrame(self, text='Choose search start date', padding=10)
        choose_start_date_frame.grid(row=1, column=0)
        start_date_cal = Calendar(choose_start_date_frame, selectmode='day', showweeknumbers=False,
                                  date_pattern='d-m-y')
        start_date_cal.grid(row=0, column=0)

        # end search date
        choose_end_date_frame = ttk.LabelFrame(self, text='Choose search end date', padding=10)
        choose_end_date_frame.grid(row=1, column=1)
        end_date_cal = Calendar(choose_end_date_frame, selectmode='day', showweeknumbers=False, date_pattern='d-m-y')
        end_date_cal.grid(row=0, column=0)

        # browser checkbox
        choose_browser_frame = ttk.LabelFrame(self, text='Choose your browser')
        choose_browser_frame.grid(row=2, columnspan=2, sticky=tk.EW, pady=10)

        browser = tk.StringVar()
        browser.set('Chrome')
        chrome = ttk.Radiobutton(choose_browser_frame, text='Chrome', variable=browser, value='Chrome')
        mozilla = ttk.Radiobutton(choose_browser_frame, text='Mozilla', variable=browser, value='Mozilla')
        chrome.grid(row=0, column=0, sticky=tk.NSEW)
        mozilla.grid(row=0, column=1, sticky=tk.NSEW)

        # label displaying chosen browser for testing
        browser_checked = ttk.Label(choose_browser_frame)
        browser_checked.grid(row=1, columnspan=2)

        # start search button
        confirm_btn = ttk.Button(self, text='Confirm entered data',
                                 command=lambda: self.clickCofirmButton(function, browser.get(), depart_city.get(),
                                                                        dest_city.get(),
                                                                        start_date_cal.get_date(),
                                                                        end_date_cal.get_date()))
        confirm_btn.grid(row=3, columnspan=2, sticky=tk.E)

        # text - cities
        picked_cities = ttk.Label(self)
        picked_cities.grid(row=4)

    def clickCofirmButton(self, function, browser, depart_city, dest_city, search_start_date, end_search_date):
        x = function(browser, depart_city, dest_city, search_start_date, end_search_date)

    def addGreetingsLabel(self):
        greeting = ttk.Label(self,
                             text="Hello to Ryanair App!",
                             justify=tk.CENTER,
                             anchor='center',
                             background='blue',
                             font=('Adhalbar', 14),
                             foreground='yellow')
        greeting.grid(row=0, columnspan=2, sticky=tk.EW)

        return greeting

    def addEntriesForCities(self, parent):
        # one common frame for both entries
        cities_frame = ttk.Frame(self)
        cities_frame.grid(row=1, sticky=tk.EW)

        # departure city frame
        depart_city_frame = self.addLabelFrame(cities_frame, text='Choose departure city')
        depart_city_frame.grid(row=0, column=0, pady=30)

        # departure city entry (parent - cities_frame)
        depart_city = tk.StringVar()
        depart_city_widget = ttk.Entry(depart_city_frame, textvariable=depart_city)
        depart_city_widget.grid(row=0, column=0)
        depart_city.get()

        # destination city frame
        dest_city_frame = ttk.LabelFrame(cities_frame, text='Choose destination city')
        dest_city_frame.grid(row=0, column=1, pady=30)

        # destination city entry (parent - cities_frame)
        dest_city = tk.StringVar()
        dest_city_widget = ttk.Entry(dest_city_frame, textvariable=dest_city)
        dest_city_widget.grid(row=0, column=1)
        depart_city.get()

    def addLabelFrame(self, parent, text, row, col):
        label_frame = ttk.LabelFrame(parent, text=text, padding=10)
        label_frame.grid(row=row, column=col)

        return label_frame

    def addCalendar(self, parent, text):
        # start search date
        choose_start_date_frame = self.addLabelFrame(parent, text='Choose search start date', padding=10, row=1, col=0)
        start_date_cal = Calendar(choose_start_date_frame, selectmode='day', showweeknumbers=False,
                                  date_pattern='d-m-y')
        start_date_cal.grid(row=0, column=0)

        # end search date
        choose_end_date_frame = ttk.LabelFrame(self, text='Choose search end date', padding=10)
        choose_end_date_frame.grid(row=1, column=1)
        end_date_cal = Calendar(choose_end_date_frame, selectmode='day', showweeknumbers=False, date_pattern='d-m-y')
        end_date_cal.grid(row=0, column=0)

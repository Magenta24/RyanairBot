import tkinter as tk
from tkinter import ttk
from .MainFrame import MainFrame
from ttkthemes import ThemedTk


class RyanairGUI(ThemedTk):

    def __init__(self, function_to_the_bot):
        super().__init__()
        self.set_theme('adapta')
        self.title('Ryanair Bot App')
        self.geometry("600x600")
        self.resizable()
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # importing new style and using it
        # self.tk.call('lappend', 'auto_path', 'awthemes-10.4.0')
        # self.tk.call('package', 'require', 'awdark')
        # s = ttk.Style()
        # s.theme_use('awdark')

        # container (parent - root)
        container = self.addMaiContainer()

        # greetings
        self.addGreetingsLabel(container)

        main_frame = MainFrame(container, 1, function_to_the_bot)

        self.mainloop()

    def addGreetingsLabel(self, parent):
        greeting = ttk.Label(parent,
                             text="RyanairBot - Search for cheapest flight",
                             justify=tk.CENTER,
                             anchor='center',
                             background='DodgerBlue3',
                             font=('Century Schoolbook', 14),
                             foreground='yellow')
        greeting.grid(row=0, sticky=tk.EW)

        return greeting

    def addMaiContainer(self):
        """
        Main container storing main page with all the widgets

        :return: container frame
        """
        container = ttk.Frame(self)
        container.grid(sticky=tk.NSEW)

        return container

    def importDarkTheme(self, root):
        # importing new style and using it
        root.tk.call('lappend', 'auto_path', 'awthemes-10.4.0')
        root.tk.call('package', 'require', 'awdark')
        s = ttk.Style()
        s.theme_use('awdark')

from Tkinter import *
from src.enums import GUI_FONT_SIZE

class Gui(object):
    """
    class for running the program as a gui
    """

    def __init__(self, master):
        """
        initialize the gui

        :param master: tkinter root object
        """
        self.master = master
        # TODO: make fullscreen
        frame = Frame(master)
        frame.pack()

        self.city = StringVar()

        self.label = Label(
            frame,
            textvariable=self.city,
            bg="black",
            fg="white",
            font=("Helvetica", GUI_FONT_SIZE)
        )

        self.label.pack()

    def update_city(self, new_city_name):
        """
        update the city displayed
        
        :param new_city_name: the new city name to display
        """
        self.city.set(new_city_name)
        self.master.update_idletasks()
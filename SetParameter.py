#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# written by Shotaro Fujimoto

from Tkinter import Tk, Frame, Label, Button, Entry, E, END


class SetParameter():

    def show_setting_window(self, parameters, commands):
        """ Show a parameter setting window.

        parameters: A list of dictionaries {'parameter name': default_value}
        commands: A list of dictionary {'name of button': command}
        """
        self.root = Tk()
        self.root.title('SetParameter')

        frame1 = Frame(self.root, padx=5, pady=5)
        frame1.pack(side='top')

        self.entry = []
        for i, parameter in enumerate(parameters):
            label = Label(frame1, text=parameter.items()[0][0] + ' = ')
            label.grid(row=i, column=0, sticky=E)
            self.entry.append(Entry(frame1, width=10))
            self.entry[i].grid(row=i, column=1)
            self.entry[i].delete(0, END)
            self.entry[i].insert(0, parameter.items()[0][1])
        self.entry[0].focus_set()

        frame2 = Frame(self.root, padx=5, pady=5)
        frame2.pack(side='bottom')

        self.button = []
        for i, command in enumerate(commands):
            self.button.append(Button(frame2, text=command.items()[0][0],
                                      command=command.items()[0][1]))
            self.button[i].grid(row=0, column=i)

        self.root.mainloop()

    def quit(self):
        self.root.destroy()

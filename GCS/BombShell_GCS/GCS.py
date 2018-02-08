#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
======================================
~Team BombShell Ground Control System~
    ~~CanSat Competition 2018~~

        Last_Edit: 1/21/2018
        Version: 0.001
======================================
Authors:
    Mason Barrow
    Nathan Ulmer
    Amber James
    
Disclaimer:
        This Ground Control Software is
    designed for use in the CanSatCompetition
    2018 exclusively by Team 5186 BombShell.
        This software is the property of team
    Bombshell and the UAH Space Hardware Club.

        The XBee Module used herin is covered
    under the Mozilla Publix License 2.0, a
    form of OpenSource Liscense. It is the
    original creation of Digi, and not ours.
    
Description:
        This software collects data from an
    XBEE radio and graphs it in real time. The
    data sent over the radio will be formated as
    follows (the NewLine characters excluded):

    <TEAM ID>,<MISSION TIME>,<PACKET COUNT>,
    <ALTITUDE>,<PRESSURE>,<TEMP>,<VOLTAGE>,
    <GPS TIME>,<GPS LATITUDE>,<GPS LONGITUDE>,
    <GPS ALTITUDE>,<GPS SATS>,<TILT X>,<TILT Y>,
    <TILT Z>,<SOFTWARE STATE>

        This data will all be in 'Engineering Units'
    and transmitted at a rate of 1hz.

    
NOTE: The XBee MUST have API mode activated through the XCTU app before this program will work.
        

'''


import tkinter as tk                #GUI Modules
from tkinter import Tk, BOTH,BOTTOM,TOP
from tkinter.ttk import Frame,Button,Label

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

from PIL import Image, ImageTk

import sys,serial,time,warnings     #System tools
from serial.serialutil import SerialException



import dataPlotter

# Verdana is good font
LARGE_FONT = ("Verdana",12)

###
# Lists to hold Data
softwareState = [0]
tiltX = [0]
tiltY = [0]
tiltZ = [0,0.1,0,-0.2,0,0.1,0,-.1,0,.1,0]
altitude = [0,1,2,4,8,16,32,64,128,256,300]
pressure = [101.325,100,99.5,99.4,99.2,99,98.9,98.7,98.8,98.6,98.5]
temp = [299.261,299.3,299.251,299.1,299.2,299.261,299.15,299.271,299.11,299.254,299.1]
voltage = [6,6,6,6,6,6,6,6,6,6,6]
teamID = [0]
packetCount = [0,1,2,3,4,5,6,7,8,9,10]
GPSTime = [0,1,2,3,4,5,6,7,8,9,10]
GPSLat = [0]
GPSLong = [0]
GPSSats = [0]
packetReceivedRate = [1,1,1,1,1,1,1,1,1,1,1]
packetsDropped = [0]
#
###



class Window(Frame):
    '''
    Tkinter window that serves as the main
    UI for the program. 
    '''
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.master.title('BombShell Ground Station Terminal v0.0001')  #Window Title
        self.grid()                                                     #Inits Grid Formatting

        self.createGraphs()
        self.createSideBar()
        self.createFooter()
        self.update()

    
    def createGraphs(self):
        self.plots = dataPlotter.Plotting_Widget()

        canvas = FigureCanvasTkAgg(self.plots.f,self)
        canvas.show()
        canvas.get_tk_widget().grid(column=0,columnspan=3,row=1)
        canvas._tkcanvas.grid(column=0,row=1)

    def createSideBar(self):
        load = Image.open('bombshell1.png').resize((210,210))
        render = ImageTk.PhotoImage(load)
       
    

        self.side_bar = Label(self,image=render,text=' ',compound=tk.BOTTOM,
                              font=LARGE_FONT,anchor=tk.NW,justify=tk.RIGHT,width=50,relief=tk.RIDGE)
        self.side_bar.image=render
        self.side_bar.grid(column=3,row=1)


    def createFooter(self):
        self.footer = Label(self,text=' ',font=LARGE_FONT,anchor=tk.SW,
                            justify=tk.LEFT,relief=tk.RIDGE,width=130)
        self.footer.grid(column = 0,row = 3,columnspan=5)
        
        
        
    def update(self):
        

        self.plots.update(GPSTime,altitude,pressure,temp,tiltZ)
        
        
        sidebar_text = "Mission Time: " + str(GPSTime[-1]) +\
                       "\nFlight State: " + str(softwareState[-1]) +\
                       "\n\nVerticle Tilt: " + str(tiltZ[-1]) +\
                       "\nAltitude: " + str(altitude[-1]) +\
                       "\nPressure: " + str(pressure[-1]) + \
                       "\nTemperature: " + str(temp[-1]) +\
                       "\n\nVoltage: " + str(voltage[-1])

        footer_text = 'Team ID: ' + str(teamID[-1]) +\
                      "\tPacket Count: " + str(packetCount[-1]) + \
                      "\tPacket Rate: " + str(packetReceivedRate[-1]) +\
                      "\tPackets Dropped: " + str(packetsDropped[-1])

        self.side_bar['text'] = sidebar_text
        self.footer['text'] = footer_text




    
def init():
    '''
    This method initializes the program and all of its instance
    variables.
    '''
    global ser,xbee,root,app
    root = Tk()
    root.geometry('1024x720+350+200')
    app = Window()

    try:
        #Initialize the Serial port for reading from the XBEE Module
        ser = serial.Serial('COM1')

        #Initialize the XBEE device using a callback
        #   The callback allows the XBEE to operate Asynchronously
        xbee = XBee(ser, callback=read_data)
    except SerialException:
        warnings.warn("COM port cannot be found. No data will be read. Try "
                      +"reconnecting the xbee.")
        

def halt():
    '''
    This method stops execution of the program and safely
    terminates all of its processes.
    '''
    xbee.halt()
    ser.close()



'''
When this program is executed
'''
if __name__ == '__main__':
    global root         #Root of the window
    
    init()              #Initialize the things

    root.mainloop()     #Starts looping the window loop
    
    halt()              #Stops execution safely
    

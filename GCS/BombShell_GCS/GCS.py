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
from tkinter import Tk, BOTH,BOTTOM,TOP,RIGHT,LEFT
from tkinter.ttk import Frame,Button,Label

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.animation as animation
from matplotlib import style

from PIL import Image, ImageTk

import sys,serial,time,warnings,csv     #System tools



#Our modules
import customWidgets  
from comms import Comms
from storage import SaveFile

# Verdana is good font
LARGE_FONT = ("Verdana",12)

#set matplotlib style
style.use('ggplot')

###
# Lists to hold Data
missionTime = [0]
softwareState = [0]
tiltX = [0]
tiltY = [0]
tiltZ = [0]
altitude = [0]
pressure = [0]
temp = [0]
voltage = [0]
teamID = [0]
packetCount = [0]
GPSTime = [0]
GPSLat = [0]
GPSLong = [0]
GPSAlt = [0]
GPSSats = [0]
packetReceivedRate = [0]
packetsDropped = [0]


data = [missionTime, packetCount,altitude,pressure,
        temp,voltage,GPSTime,GPSLat,GPSLong,GPSAlt,
        GPSSats,tiltX,tiltY,tiltZ,softwareState]
#
###




class Window(Frame):
    '''
    Tkinter window that serves as the main
    UI for the program. 
    '''
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.initUI()
        self.width = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()

    def initUI(self):
        self.master.title('BombShell Ground Station Terminal v0.0001')  #Window Title
                                                          
        self.createGraphs()                                             
        self.createSideBar()
        self.createFooter()
        self.update()
        self.bind('<Configure>',self.on_resize)

    
    def createGraphs(self):
        self.plots = customWidgets.Plotting_Widget()

        canvas = FigureCanvasTkAgg(self.plots.f,self)
        canvas.show()
       
        canvas.get_tk_widget().pack()
       
        
        self.anim = animation.FuncAnimation(self.plots.f, self.update,interval=1000)
        self.canvas=canvas

    def createSideBar(self):
        load = Image.open('bombshell1.png').resize((210,210))
        render = ImageTk.PhotoImage(load)
       
    

        self.side_bar = Label(self,image=render,text=' ',compound=tk.BOTTOM,
                              font=LARGE_FONT,anchor=tk.NE,justify=tk.RIGHT,width=50,relief=tk.RIDGE)
        self.side_bar.image=render
      
    def createFooter(self):
        self.footer = Label(self,text=' ',font=LARGE_FONT,anchor=tk.SE,
                            justify=tk.LEFT,relief=tk.RIDGE)
        
        
        
    def update(self,i=None):
        

        self.plots.update(GPSTime,altitude,pressure,temp,tiltZ) #Calls the custom plots widget to update itself and redraw the plots
        
        
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

           
        self.pack(side=TOP,fill=BOTH,expand=1)      #basically just to initialize the Frames window manager.
        self.update_idletasks()                     #Forces the Frame to update it's geometry
                                                    #(usually it handles all events and goes back to update static stuff.)


        ###This originally used .pack(), but .pack() does weird things sometimes.
        ### .pack() should onnly be used to ensure the outer-frame is ready to be drawn to
        self.footer.place(y=self.winfo_height(),x=0,anchor=tk.SW)    #Places the bottom of the footer at the bottom-left of the screen
        self.side_bar.place(x=self.winfo_width(),y=0,anchor=tk.NE)   #Places the the sidebar in the top-right corner of the scren
        self.canvas._tkcanvas.place(x=0,y=0)                         #Places graphs in top left


        self.save(data)

    def save(self,data):
        with open('telemetry.csv','a',newline='') as save_file:
            saver= csv.writer(save_file, delimiter=",",
                              quotechar='|', quoting=csv.QUOTE_NONE)

            for i in range(len(data[0])):
                row = []
                for el in data:
                    row.append(el[-1])

                saver.writerow(row)        

        
        
        
       
        



    def on_resize(self,event):
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height

        self.update()

        self.config(width = self.width,height=self.height)

        
        

    
def init():
    '''
    This method initializes the program and all of its instance
    variables.
    '''
    global ser,xbee,root,app
    root = Tk()
    root.geometry('1366x768+350+200')
    app = Window()
    xbee = Comms('COM5',data)

    with open('telemetry.csv','w',newline='') as save_file:
            saver= csv.writer(save_file, delimiter=",",
                              quotechar='|', quoting=csv.QUOTE_MINIMAL)
            row = ['missionTime', 'packetCount','altitude','pressure',
                   'temp','voltage','GPSTime','GPSLat','GPSLong','GPSAlt',
                   'GPSSats','tiltX','tiltY','tiltZ','softwareState']
            saver.writerow(row)

    
    
def halt():
    '''
    This method stops execution of the program and safely
    terminates all of its processes.
    '''
    

    


'''
When this program is executed
'''
if __name__ == '__main__':
    global root         #Root of the window
    
    init()              #Initialize the things

    app.mainloop()     #Starts looping the window loop
    
    halt()              #Stops execution safely
    

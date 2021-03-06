#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
======================================
~Team BombShell Ground Control System~
    ~~CanSat Competition 2018~~

        Created: 1/21/2018
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



''''''
######
import pyqtgraph

import tkinter as tk                #GUI Modules
from tkinter import Tk, BOTH,BOTTOM,TOP,RIGHT,LEFT
from tkinter.ttk import Frame,Button,Label,Menubutton,Notebook

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.animation as animation
from matplotlib import style

from PIL import Image, ImageTk

import sys,serial,time,warnings,csv     #System tools
######
''''''



###Our modules###
import customWidgets  
from comms import Comms
from storage import SaveFile

###Verdana is good font###
LARGE_FONT = ("Verdana",12)

###set matplotlib style###
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

save_file=None

data = [teamID,missionTime, packetCount,altitude,pressure,
        temp,voltage,GPSTime,GPSLat,GPSLong,GPSAlt,
        GPSSats,tiltX,tiltY,tiltZ,softwareState]

raw_data = []
#
###




class Window(Frame):
    '''
    # Window
    #
    # @Inherets Tkinter Frame class
    #
    # This is the main object that represents the GCS  
    '''
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.initUI()
        self.width = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()

    #Upper Lebel method which calls all init functions for the window
    def initUI(self):
        self.master.title('BombShell Ground Station Terminal v0.0001')  #Window Title
                                                          
        self.createGraphs()         #Creates all graphs within a Notebook context                                   
        self.createSideBar()        #Creates a permanent side-bar to display some data
        self.createFooter()         #Same but for a footer
        self.update()               
       


    #Creates all graphs within a Notebook context  
    def createGraphs(self):

        #Notebook to hold tab frames
        self.nb = Notebook(self)

        #Frame to hold the MatplotLib plotting widgets
        page1 = Frame(self.nb,width = 300, height = self.winfo_reqwidth())
        page2 = Frame(self.nb,width = 300, height = self.winfo_reqwidth())

        #Each plotting widget with MatplotLib
        self.plots1 = customWidgets.Plotting_Widget()
        self.plots2 = customWidgets.Plotting_Widget_2()

        #Adds each plot to a canvas to draw, then it shows them
        canvas1 = FigureCanvasTkAgg(self.plots1.f,page1)
        canvas2 = FigureCanvasTkAgg(self.plots2.f,page2)
        canvas1.show()
        canvas2.show()

        #packs the canvases
        canvas1.get_tk_widget().pack()
        canvas2.get_tk_widget().pack()

        #adds the pages to the notebook context
        self.nb.add(page1,text='Main Telemetry')
        self.nb.add(page2,text='Other Telemetry')
        
        #Animates the Graphs
        self.anim1 = animation.FuncAnimation(self.plots1.f, self.update,interval=1000)
        self.anim2 = animation.FuncAnimation(self.plots2.f,self.update,interval=3500)

        self.canvas1 = canvas1
        self.canvas2 = canvas2
        

    def createSideBar(self):
        
        load = Image.open('bombshell1.png').resize((210,210))
        render = ImageTk.PhotoImage(load)

        O_RESET = Button(self,text='*RESET MCU*', command=ResetCallback)
        O_FS0 = Button(self,text='Set Flight State 0',command=FS0Callback)
        O_FS1 = Button(self,text='Set Flight State 1',command=FS1Callback)
        O_FS2 = Button(self,text='Set Flight State 2',command=FS2Callback)
        O_FS3 = Button(self,text='Set Flight State 3',command=FS3Callback)
        O_DepHS = Button(self,text='Deploy Heatshield', command=DepHSCallback)
        O_DetHS = Button(self,text='Detatch Heatshield', command=DetHSCallback)
        O_DepParachute= Button(self,text='Deploy Parachute', command=DepParachuteCallback)
        O_BuzzOn = Button(self,text='Buzzer ON', command=BuzzOn)
        O_BuzzOff = Button(self,text='Buzzer OFF',command=BuzzOff)
        O_Calibrate = Button(self,text='Calibrate Gyro',command=Calibrate)
        
        self.overrideButtons = [O_RESET,O_FS0,O_FS1,O_FS2,O_FS3,O_DepHS,O_DetHS,O_DepParachute,O_BuzzOn,O_BuzzOff,O_Calibrate]
        
        
        
        self.side_bar = Label(self,image=render,text=' ',compound=tk.BOTTOM,
                              font=LARGE_FONT,anchor=tk.NE,justify=tk.RIGHT,relief=tk.RIDGE)
        self.side_bar.image=render

        
        
      
    def createFooter(self):
        self.footer = Label(self,text=' ',font=LARGE_FONT,anchor=tk.SE,
                            justify=tk.LEFT,relief=tk.RIDGE)
        
        
        
    def update(self,i=None):
       # xbee.rx(data)
        
        self.plots1.update(data) #Calls the custom plots widget to update itself and redraw the plots
        self.plots2.update(data)
        #print("all clear")
        
        sidebar_text = "Mission Time: " + str(data[1][-1]) +\
                       "\nFlight State: " + str(data[15][-1]) +\
                       "\n\nVerticle Tilt: " + str(data[14][-1]) +\
                       "\nAltitude: " + str(data[3][-1]) +\
                       "\nPressure: " + str(data[4][-1]) + \
                       "\nTemperature: " + str(data[5][-1]) +\
                       "\n\nVoltage: " + str(data[6][-1]) #+\
                       #"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"

        footer_text = 'Team ID: ' + str(teamID[-1]) +\
                      "\tPacket Count: " + str(data[2][-1]) + \
                      "\tPacket Rate: " + str(packetReceivedRate[-1]) +\
                      "\tPackets Dropped: " + str(packetsDropped[-1]) +\
                      "                                             " +\
                      "                                             " +\
                      "                              "

        self.side_bar['text'] = sidebar_text
        self.footer['text'] = footer_text

           
        self.pack(side=TOP,fill=BOTH,expand=1)      #basically just to initialize the Frames window manager.
        self.update_idletasks()                     #Forces the Frame to update it's geometry
                                                    #(usually it handles all events and goes back to update static stuff.)


        ###This originally used .pack(), but .pack() does weird things sometimes.
        ### .pack() should onnly be used to ensure the outer-frame is ready to be drawn to
        self.footer.place(y=self.winfo_height(),x=0,anchor=tk.SW)    #Places the bottom of the footer at the bottom-left of the screen
        self.side_bar.place(x=self.winfo_width(),y=self.winfo_height()-20,anchor=tk.SE)   #Places the the sidebar in the top-right corner of the scren
        self.canvas1._tkcanvas.place(x=0,y=0)                         #Places graphs in top left
        self.canvas2._tkcanvas.place(x=0,y=0)                         #Places graphs in top left                                            
        self.nb.place(x=0,y=0)
       
        height = 20
        for b in self.overrideButtons:
            b.place(x=self.winfo_width()-200,y=height,anchor=tk.NW)
            height +=30
        
        self.save(data)

    def save(self,data):
        global save_file
       # print(save_file)
        saver= csv.writer(save_file, delimiter=",",
                          quotechar='|', quoting=csv.QUOTE_NONE,escapechar='\\')
        

        for i in range(len(data[0])):
            row = []
            for el in data:
                row.append(el[-1])

            saver.writerow(row)        

        
        
        
       
        



    

        
        

    
def init():
    '''
    This method initializes the program and all of its instance
    variables.
    '''
    global ser,xbee,root,app,save_file
    xbee = Comms('COM5',data,raw_data)

    try:
        save_file = open('telemetry.csv','w',newline='')
        
        saver= csv.writer(save_file, delimiter=",",
                          quotechar='|', quoting=csv.QUOTE_MINIMAL,escapechar='\\')
        row = ['Team ID', 'missionTime', 'packetCount','altitude','pressure',
               'temp','voltage','GPSTime','GPSLat','GPSLong','GPSAlt',
               'GPSSats','tiltX','tiltY','tiltZ','softwareState']
        saver.writerow(row)
        save_file.close()
        save_file = open('telemetry.csv','a',newline='')
    except Exception:
        print('file error')
    
    root = Tk()
    root.geometry('1366x768+350+200')
    app = Window()
    

    
    
    
def halt():
    '''
    This method stops execution of the program and safely
    terminates all of its processes.
    '''
    global save_file
    #xbee.halt()
    xbee.halt()
    save_file.close()

    
def ResetCallback():
    xbee.tx('!')
    print('!')

def FS0Callback():
    xbee.tx('@')
    print('!')

def FS1Callback():
    xbee.tx('#')
    print('!')

def FS2Callback():
    xbee.tx('$')
    print('!')

def FS3Callback():
    xbee.tx('%')
    print('!')
def DepHSCallback():
    xbee.tx('^')
    print('!')
def DetHSCallback():
    xbee.tx('*')
    print('!')
def DepParachuteCallback():
    xbee.tx('&')
    print('!')
def BuzzOn():
    xbee.tx('(')
    print('!')
def BuzzOff():
    xbee.tx(')')
    print('!')
def Calibrate():
    xbee.tx('_')
    print('!')
    

'''
When this program is executed
'''
if __name__ == '__main__':
    global root         #Root of the window
    
    init()              #Initialize the things

    app.mainloop()     #Starts looping the window loop
    
    halt()              #Stops execution safely
    

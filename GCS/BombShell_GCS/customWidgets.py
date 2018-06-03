import matplotlib
from matplotlib.backends import backend_tkagg
from matplotlib.figure import Figure
matplotlib.use("TkAgg")


"""
This widget contains the plots of altitude, pressure, temp, and tiltz.
These are the mmission critical data, and appear on the main page of the GCS.
"""
class Plotting_Widget:
    def __init__(self):

        #Creates Figure and subplot
        f = Figure(figsize=(11,10),dpi=70)
        self.altitude_plot=f.add_subplot(221)
        self.pressure_plot=f.add_subplot(222)
        self.temp_plot=f.add_subplot(223)
        self.tiltZ_plot=f.add_subplot(224)
        
        #List of plots to make code more readable
        self.plots = [self.altitude_plot,self.pressure_plot,
                 self.temp_plot,self.tiltZ_plot]

        #finishes the initialization of the plots
        self.clear_and_label_plots()
        
        self.f = f

    '''
    Clears the plots then plots the updated data received from the probe
    '''
    def update(self,GPSTime, altitude,pressure,temp,tiltZ):
       
        
        self.clear_and_label_plots()

        #Plots time vs. each peice of data
        self.altitude_plot.plot(GPSTime,altitude)
        self.pressure_plot.plot(GPSTime,pressure)
        self.temp_plot.plot(GPSTime,temp)
        self.tiltZ_plot.plot(GPSTime,tiltZ)
        


    '''
    Clears the data from the plots so that the data doesn't overlap
    as it comes in. Then it relabels the plots because clearing them
    removew their formatting.
    '''
    def clear_and_label_plots(self):
        for plot in self.plots:
            plot.clear()
        

        self.altitude_plot.set_title('Altitude')
        self.altitude_plot.set_xlabel('Time (s)')
        self.altitude_plot.set_ylabel('meters')

        self.pressure_plot.set_title('Pressure')
        self.pressure_plot.set_xlabel('Time (s)')
        self.pressure_plot.set_ylabel('KPa')

        self.temp_plot.set_title('Temperature')
        self.temp_plot.set_xlabel('Time (s)')
        self.temp_plot.set_ylabel('Kelvin')

        self.tiltZ_plot.set_title('Tilt from Vertical')
        self.tiltZ_plot.set_xlabel('Time (s)')
        self.tiltZ_plot.set_ylabel('Degrees from Z axis')

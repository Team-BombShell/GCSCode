import matplotlib
from matplotlib.backends import backend_tkagg
from matplotlib.figure import Figure
matplotlib.use("TkAgg")

class Plotting_Widget:
    def __init__(self):
        f = Figure(figsize=(11,10),dpi=70)
        self.altitude_plot=f.add_subplot(221)
        self.pressure_plot=f.add_subplot(222)
        self.temp_plot=f.add_subplot(223)
        self.tiltZ_plot=f.add_subplot(224)

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


        self.f = f

    def update(self,GPSTime, altitude,pressure,temp,tiltZ):
        self.altitude_plot.plot(GPSTime,altitude)
        self.pressure_plot.plot(GPSTime,pressure)
        self.temp_plot.plot(GPSTime,temp)
        self.tiltZ_plot.plot(GPSTime,tiltZ)



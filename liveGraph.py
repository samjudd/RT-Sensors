import matplotlib

matplotlib.use('TKAgg')

import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import datetime
import time
from fake_labjack import u3
from thermocouple_convert import ThermocoupleConverter
from LabJackSensor import PressureSensor
#import threading #use to make function loop every x seconds 

class Graph:
    '''Class for displaying the 3 subplots in real time for the hot fire test
	The plots are: Pressure in gauge psi and Force in Newtons'''

    def __init__(self):
        self.interval = 1  # milliseconds per sample
        self.length = 100  # saved points
        self.t = [-float(self.interval) / 1000 * k for k in range(self.length, 0, -1)]
        
        #set input pins
        self.Force1pin = 1
        self.Force2pin = 2
        self.Force3pin = 3
        self.Pressure1pin = 4
        self.Pressure2pin = 5
        self.Pressure3pin = 6
        self.Temp1pin = 3

	#set length of pressure record
        self.pressure1 = [0] * self.length
        self.pressure2 = [0] * self.length
        self.pressure3 = [0] * self.length
	
	#set length of force record
        self.force1 = [0] * self.length
        self.force2 = [0] * self.length
        self.force3 = [0] * self.length
        
        #set length of temperature record
        self.temp1 = [0] * self.length

        # Creates the "logs" folder if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # creates a file in "logs" folder, with format "Year-Month-Day__Hour-Minute-Second"
        self.log = open('logs/%s.txt' % time.strftime("%Y-%m-%d__%H-%M-%S"), 'wb')
        self.time = time.time()
        self.log.write('sample_time, force1, force2, force3, pressure1, pressure2, pressure3, temp1\n')

	#initialize labjack object, configure it, and set the FIO ports to analog read
        self.d = u3.U3()
        self.d.configU3()
        self.d.getCalibrationData()
        self.d.configIO(FIOAnalog=255)
        
	#arrange plots in 3 rows and 1 column
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(nrows=3, ncols=1)

	#adjust location of plots in window
        plt.subplots_adjust(bottom=0.05, top=0.95, left=0.05, right=0.85)

	#label each plot on the y axis
        self.ax1.set_ylabel('Pressure (psi)')
        self.ax2.set_ylabel('Force (N)')
        self.ax3.set_ylabel('Temperature (deg C)')
	
	#set the limits of the axes, this needs to change
        self.ax1.set_ylim([0, 10e6])
        self.ax2.set_ylim([-5, 5])
        self.ax3.set_ylim([0,2000])

	#array of zeros to hold points
        y = [0] * self.length

	# #make pressure lines on plots
 #        self.pressureLine1 = self.ax1.plot(self.t, y, color='orange', label="Fuel Pressure")[0]
 #        self.pressureLine2 = self.ax1.plot(self.t, y, color='green', label="Ox Pressure")[0]
 #        self.pressureLine3 = self.ax1.plot(self.t, y, color='red', label="Chmb Pressure")[0]
	
	# #make force lines on plots
 #        self.forceLine1 = self.ax2.plot(self.t, y, label="Force 1")[0]
 #        self.forceLine2 = self.ax2.plot(self.t, y, label="Force 2")[0]
 #        self.forceLine3 = self.ax2.plot(self.t, y, label="Force 3")[0]
        
 #        #make temperature line on plot
 #        self.tempLine1 = self.ax3.plot(self.t, y, label='Temp 1')[0]

	
        # Temperature data conversion
        # self.tc = ThermocoupleConverter('thermocouple_type_B.csv')

        self.sensors = []
        pins = [4,5,6]
        names = ['Chamber', 'Ox', 'Fuel']
        colors = ['orange', 'green', 'red']
        for pin, name, color in zip(pins, names, colors):
            ps = PressureSensor(self.d, pin, name, 1.0, 34.47e6/4.0)
            # line and record are tecked on here, they are not typically sensor
            # class attributes.
            ps.line = self.ax1.plot(self.t, y, color=color, label=name)[0]
            ps.record = [0] * self.length
            self.sensors.append(ps)
        
        #make the legend look nice  
        self.ax1.legend(bbox_to_anchor=(1.0, 0.5), loc='center left', prop={'size': 10})
        # self.ax2.legend(bbox_to_anchor=(1.0, 0.5), loc='center left', prop={'size': 10})
        # self.ax3.legend(bbox_to_anchor=(1.0, 0.5), loc='center left', prop={'size': 10})


    # Start time
        self.start_time = datetime.datetime.now()

    def readData(self):
        '''read data from Labjack and save the most recent values'''

        # sample time
        sample_time =(datetime.datetime.now() - self.start_time).total_seconds()

        for sensor in self.sensors:
            new_value = sensor.convert_raw(sensor.read_raw())
            sensor.record = sensor.record[1:] + [new_value]       


    def init(self):
        '''Function for initializing the graph. Called by FuncAnimation'''

        y = [0] * self.length
        lines = []
        for sensor in self.sensors:
            sensor.line.set_data(self.t, y)
            lines.append(sensor.line)

        return lines

    def animate(self, i):
        '''Updates the graph. i is the frame number, which is ignored'''
        self.time = time.time()

        self.readData()

        lines = []
        for sensor in self.sensors:
            sensor.line.set_ydata(sensor.record)
            lines.append(sensor.line)

        return lines

    def show(self):
        ani = animation.FuncAnimation(self.fig, self.animate, frames=1, interval=self.interval, blit=True,
                                      init_func=self.init)
        plt.show()


if __name__ == '__main__':
    g = Graph()
    g.show()

import matplotlib

matplotlib.use('TKAgg')

import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import datetime
import time
import u3
from thermocouple_convert import ThermocoupleConverter
#import threading #use to make function loop every x seconds 

class Graph:
    '''Class for displaying the 3 subplots in real time for the hot fire test
	The plots are: Pressure in gauge psi and Force in Newtons'''

    def __init__(self):
        self.interval = 30  # milliseconds per sample
        self.length = 100  # saved points
        self.t = [-float(self.interval) / 1000 * k for k in range(self.length, 0, -1)]
        
        #set input pins
        self.Force1pin = 6
        self.Force2pin = 1
        self.Force3pin = 2
        self.Pressure1pin = 4
        self.Pressure2pin = 5
        self.Temp1pin = 0

	#set length of pressure record
        self.pressure1 = [0] * self.length
        self.pressure2 = [0] * self.length
	
	#set length of force record
        self.force1 = [0] * self.length
        self.force2 = [0] * self.length
        self.force3 = [0] * self.length
        
        #set length of temperature record
        self.temp1 = [0] * self.length

        # Creates the "logs" folder if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # creates a file in "logs" folder, with format "Day-Month-Year__Hour-Minute-Second"
        # eg. 10/10/2014 12:51:30 AM is "10-10-2014__00-51-30"
        self.log = open('logs/%s.txt' % time.strftime("%d-%m-%Y__%H-%M-%S"), 'wb')
        self.time = time.time()

	#initialize labjack object, configure it, and set the FIO ports to analog read
        self.d = u3.U3()
        self.d.configU3()
        self.d.getCalibrationData()
        self.d.configIO(FIOAnalog=255)
        
	#arrange plots in 3 rows and 1 column
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(nrows=3, ncols=1)

	#adjust location of plots in window
        plt.subplots_adjust(bottom=0.05, top=0.95, left=0.05, right=0.9)

	#label each plot on the y axis
        self.ax1.set_ylabel('Pressure (psi)')
        self.ax2.set_ylabel('Force (N)')
        self.ax3.set_ylabel('Temperature (deg C)')
	
	#set the limits of the axes, this needs to change
        self.ax1.set_ylim([0, 5])
        self.ax2.set_ylim([-5, 5])
        self.ax3.set_ylim([0,2000])

	#array of zeros to hold points
        y = [0] * self.length

	#make pressure lines on plots
        self.pressureLine1 = self.ax1.plot(self.t, y, label="Pressure 1")[0]
        self.pressureLine2 = self.ax1.plot(self.t, y, label="Pressure 2")[0]
	
	#make force lines on plots
        self.forceLine1 = self.ax2.plot(self.t, y, label="Force 1")[0]
        self.forceLine2 = self.ax2.plot(self.t, y, label="Force 2")[0]
        self.forceLine3 = self.ax2.plot(self.t, y, label="Force 3")[0]
        
        #make temperature line on plot
        self.tempLine1 = self.ax3.plot(self.t, y, label='Temp 1')[0]

	#make the legend look nice	
        self.ax1.legend(bbox_to_anchor=(1.0, 0.5), loc='center left', prop={'size': 10})
        self.ax2.legend(bbox_to_anchor=(1.0, 0.5), loc='center left', prop={'size': 10})
        self.ax3.legend(bbox_to_anchor=(1.0, 0.5), loc='center left', prop={'size': 10})

        # Temperature data conversion
        self.tc = ThermocoupleConverter('thermocouple_type_B.csv')

    def readData(self):
        '''read data from Labjack and save the most recent values'''

        # The load cell is rated for 300lb with an output of 2mV / V
        # We must first calibrate the cells to read 0 when the engine
        # is attached but not firing
        # offset = ???
        # gain =
        # scale = .002
        # nominal = 300

	#get force readings (in volts) from labjack
        force1_v = self.d.getAIN(self.Force1pin)
        force2_v = self.d.getAIN(self.Force2pin)
        force3_v = self.d.getAIN(self.Force3pin)

	#get pressure readings (in volts) from labjack
        pressure1_v = self.d.getAIN(self.Pressure1pin)
        pressure2_v = self.d.getAIN(self.Pressure2pin)
        
        #get temperature readings (in volts) from labjack
        temp1_v = self.d.getAIN(self.Temp1pin)        
        
        #using calibrations from earlier, convert the voltage readings to meaningful data 
        #JOHANNES REPLACE THE 1s with actual things
        force1 = force1_v * 1
        force2 = force2_v * 1
        force3 = force3_v * 1
        
        pressure1 = pressure1_v * 1
        pressure2 = pressure2_v * 1
        
        if temp1_v < 0:
            temp1_v = 0
        temp1 = self.tc.get_temperature(temp1_v / 368.36)
        print 'temp1_v = %.3f volts amplified, %.1f K' % (temp1_v, temp1)
        
        sample = [force1, force2, force3, pressure1, pressure2, temp1]

	#write sample to log
        logString = ','.join(map(str, sample))
        self.log.write(logString + '\n')
        
        self.force1 = self.force1[1:] + [force1]
        self.force2 = self.force2[1:] + [force2]
        self.force3 = self.force3[1:] + [force3]

        self.pressure1 = self.pressure1[1:] + [pressure1]
        self.pressure2 = self.pressure2[1:] + [pressure2]
        
        self.temp1 = self.temp1[1:] + [temp1]


    def init(self):
        '''Function for initializing the graph. Called by FuncAnimation'''

        y = [0] * self.length
	
	#initializes the graph to the inital values
	self.forceLine1.set_data(self.t, y)
        self.forceLine2.set_data(self.t, y)
        self.forceLine3.set_data(self.t, y)
	
        self.pressureLine1.set_data(self.t, y)
        self.pressureLine2.set_data(self.t, y)
        
        self.tempLine1.set_data(self.t, y)

        return [self.forceLine1, self.forceLine2, self.forceLine3, self.pressureLine1, self.pressureLine2, self.tempLine1]


    def animate(self, i):
        '''Updates the graph. i is the frame number, which is ignored'''
        self.time = time.time()

        self.readData()
	
	#plots the current data

        self.forceLine1.set_ydata(self.force1)
        self.forceLine2.set_ydata(self.force2)
        self.forceLine3.set_ydata(self.force3)
        
        self.pressureLine1.set_ydata(self.pressure1)
        self.pressureLine2.set_ydata(self.pressure2)
        
        self.tempLine1.set_ydata(self.temp1)

        return [self.forceLine1, self.forceLine2, self.forceLine3, self.pressureLine1, self.pressureLine2, self.tempLine1]


    def show(self):
        ani = animation.FuncAnimation(self.fig, self.animate, frames=1, interval=self.interval, blit=True,
                                      init_func=self.init)
        plt.show()


if __name__ == '__main__':
    g = Graph()
    g.show()

import matplotlib
matplotlib.use('TKAgg')

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import datetime
import time
import u3


class Graph:
	'''Class for displaying the 3 subplots in real time for the hot fire test
	The plots are: Pressure, Gas concentrations, and force'''

	def __init__(self):
		self.interval = 30 #milliseconds per sample
		self.length = 100 #saved points
		self.t = [-float(self.interval)/1000 * k for k in range(self.length, 0, -1)]


		self.pressure1 = [0] * self.length
		# self.pressure2 = [0] * self.length
		#
		# self.gas1 = [0] * self.length
		# self.gas2 = [0] * self.length
		# self.gas3 = [0] * self.length

		self.force1 = [0] * self.length
		self.force2 = [0] * self.length
		self.force3 = [0] * self.length

		self.log = open('logs/%s.txt' % datetime.datetime.now(), 'wb')
		self.time = time.time()


		self.d = u3.U3()
		self.d.configU3()
		self.d.getCalibrationData()
		self.d.configIO(FIOAnalog=255)

		# self.fig, axes = plt.subplots(nrows=3, ncols=1)
		# (self.ax1, self.ax2, self.ax3) = axes
		self.fig, (self.ax1, self.ax3) = plt.subplots(nrows=2, ncols=1)

		plt.subplots_adjust(bottom=0.05, top=0.95, left=0.05, right=0.9)


		self.ax1.set_ylabel('Pressure (psi)')
		# self.ax2.set_ylabel('Concentration (ppm)')
		self.ax3.set_ylabel('Force (N)')


		self.ax1.set_ylim([0,5])
		# self.ax2.set_ylim([0,5])
		self.ax3.set_ylim([-5,5])

		y = [0] * self.length

		self.pressureLine1 = self.ax1.plot(self.t, y, label="Pressure 1")[0]
		# self.pressureLine2 = self.ax1.plot(self.t, y, label="Pressure 1")[0]
		#
		# self.gasLine1 = self.ax2.plot(self.t, y, label="Gas 1")[0]
		# self.gasLine2 = self.ax2.plot(self.t, y, label="Gas 2")[0]
		# self.gasLine3 = self.ax2.plot(self.t, y, label="Gas 3")[0]

		self.forceLine1 = self.ax3.plot(self.t, y, label="Force 1")[0]
		self.forceLine2 = self.ax3.plot(self.t, y, label="Force 2")[0]
		self.forceLine3 = self.ax3.plot(self.t, y, label="Force 3")[0]

		self.ax1.legend(bbox_to_anchor = (1.0, 0.5), loc='center left', prop={'size':10})
		# self.ax2.legend(bbox_to_anchor = (1.0, 0.5), loc='center left', prop={'size':10})
		self.ax3.legend(bbox_to_anchor = (1.0, 0.5), loc='center left', prop={'size':10})
		# plt.tight_layout()



	def readData(self):
		'''read data from Labjack and save the most recent values'''



		# pressure1 = random.random()
		# pressure2 = random.random()

		# gas1 = random.random()
		# gas2 = random.random()
		# gas3 = random.random()

		# force1 = random.random()
		# force2 = random.random()
		# force3 = random.random()


		# The load cell is rated for 300lb with an output of 2mV / V
		# We must first calibrate the cells to read 0 when the engine
		# is attached but not firing
		# offset = ???
		# gain =
		# scale = .002
		# nominal = 300

		force1 = self.d.getAIN(0)
		force2 = self.d.getAIN(1)
		force3 = self.d.getAIN(2)

		pressure1 = self.d.getAIN(4)
		# pressure2 = self.d.getAIN(4)
		#
		# gas1 = self.d.getAIN(5)
		# gas2 = self.d.getAIN(6)
		# gas3 = self.d.getAIN(7)



		# sample = [pressure1, pressure2, gas1, gas2, gas3, force1, force2, force3]
		sample = [pressure1, force1, force2, force3]

		logString = ','.join(map(str, sample))
		self.log.write(logString+'\n')


		self.pressure1 = self.pressure1[1:] + [pressure1]
		# self.pressure2 = self.pressure2[1:] + [pressure2]
		#
		# self.gas1 = self.gas1[1:] + [gas1]
		# self.gas2 = self.gas2[1:] + [gas2]
		# self.gas3 = self.gas3[1:] + [gas3]

		self.force1 = self.force1[1:] + [force1]
		self.force2 = self.force2[1:] + [force2]
		self.force3 = self.force3[1:] + [force3]


	def init(self):
		'''Function for initializing the graph. Called by FuncAnimation'''

		y = [0] * self.length

		self.pressureLine1.set_data(self.t, y)
		# self.pressureLine2.set_data(self.t, y)
		#
		# self.gasLine1.set_data(self.t, y)
		# self.gasLine2.set_data(self.t, y)
		# self.gasLine3.set_data(self.t, y)

		self.forceLine1.set_data(self.t, y)
		self.forceLine2.set_data(self.t, y)
		self.forceLine3.set_data(self.t, y)

		# return [self.pressureLine1, self.pressureLine2, self.gasLine1, \
		# 		self.gasLine2, self.gasLine3, \
		# 		self.forceLine1, self.forceLine2, self.forceLine3]

		return [self.pressureLine1, self.forceLine1, self.forceLine2, self.forceLine3]



	def animate(self, i):
		'''Updates the graph. i is the frame number, which is ignored'''
		now = time.time()
		# print 'dt:', now - self.time
		self.time = now

		self.readData()

		self.pressureLine1.set_ydata(self.pressure1)
		# self.pressureLine2.set_ydata(self.pressure2)
		#
		# self.gasLine1.set_ydata(self.gas1)
		# self.gasLine2.set_ydata(self.gas2)
		# self.gasLine3.set_ydata(self.gas3)

		self.forceLine1.set_ydata(self.force1)
		self.forceLine2.set_ydata(self.force2)
		self.forceLine3.set_ydata(self.force3)

		# return [self.pressureLine1, self.pressureLine2, self.gasLine1, \
		# 		self.gasLine2, self.gasLine3, \
		# 		self.forceLine1, self.forceLine2, self.forceLine3]

		return [self.pressureLine1, self.forceLine1, self.forceLine2, self.forceLine3]



	def show(self):
		ani = animation.FuncAnimation(self.fig, self.animate, frames=1, interval=self.interval, blit=True, init_func=self.init)
		plt.show()

if __name__ == '__main__':
	g = Graph()
	g.show()

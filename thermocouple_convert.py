import os.path
import numpy as np

class ThermocoupleConverter():
	def __init__(self, table_name):
		""" Load a new Temprature-voltage table.

		:param table_name: The name of the CSV file to load the table data from.
		:type table_name: str.
		:raises: IOError, TypeError, ValueError.
		"""
		# Check that the substance param is a string.
		if not isinstance(table_name, basestring):
			raise TypeError("table_name must be a string.")
		# Check if we have a table file for this table_name.
		if not os.path.isfile(table_name):
			raise ValueError("No table file exists for the table_name %s."%(table_name))
		# Load data from the table file.
		table = np.genfromtxt(table_name, delimiter=",")
		self.table = table[1:,:]
		self.voltage = table[1:,0]
		self.n = self.voltage.size

	def _get(self, voltage, which):
		# Raise an exception if the voltage is too low
		if voltage < self.voltage[0]:
			raise ValueError("The voltage %.3f is below the table minimum"\
				%(voltage))
		# Raise an exception if the temp is too high
		if voltage > self.voltage[-1]:
			raise ValueError("The voltage %.3f is above the table maximum"\
				%(voltage))
		for i in xrange(1,self.n):
			if voltage == self.voltage[i]:
				return self.table[i, which]
			if voltage < self.voltage[i]:
				# linearly interpolate between the two nearest values in the table.
				x = (voltage- self.voltage[i-1])/(self.voltage[i] - self.voltage[i-1])
				value = self.table[i-1, which] + x*(self.table[i, which] - self.table[i-1, which])
				return value

	def get_temperature(self, voltage):
		""" Get the temeprature for a voltage reading.
		    :param voltage: The unamplified thermocouple output voltage [volts]
		    :returns: temperature [Kelvin]
		    """
		return self._get(voltage, 1)


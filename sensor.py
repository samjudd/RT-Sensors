class Sensor(object):
	def __init__(self):
		# The latest raw readign from the sensor
		self.latest_raw_value = None
		# The name of the sensor channel (e.g. 'Chamber pressure')
		self.name = ''
		# The type of sensor (e.g. 'pressure', 'force', 'temperature')
		self.type = ''
		# The physical units of the sensor's raw reading (e.g. 'volts')
		self.raw_units = ''
		# The physical units of the sensor's converted reading (e.g. 'pascal', 'newton')
		self.converted_units = ''
		# Senor status. True if the sensor is functioning properly and reading valid values.
		self.valid_status = False

	def read_raw(self):
		""" Read a new raw value from the sensor hardware interface. """
		pass

	def convert_raw(self, raw):
		""" Convert a raw sensor reading (i.e. volts) to physical units. """
		pass

	def get_raw(self):
		""" Get the latest raw value (without reading from the hardware). """
		return self.latest_raw_value

	def get_converted(self):
		""" Get the latest converted (i.e. physical units) value (without reading from the hardware). """
		return self.convert_raw(self.latest_value)

from sensor import Sensor
from LabJackPython import LabJackException

class LabJackSensor(Sensor):
	def __init__(self, lab_jack, pin):
		""" Create a new LabJackSensor.
		:param lab_jack: Lab Jack Analog to Digital converter object, see http://labjack.com/support/labjackpython.
		:type lab_jack: u3
		:param pin: The analog input pin on the LabJack which the sensor's signal is connected to.
		:type pin: integer >= 0
		"""
		self.lab_jack = lab_jack
		if pin < 0:
			raise ValueError('LabJack analog input pin for sensor must be nonnegative')
		self.pin = pin
		super(LabJackSensor, self).__init__()

	def read_raw(self):
		""" Read a new raw value from the sensor hardware interface. 
		Overrides fucntion in Sensor. """
		try:
			self.latest_raw_value = self.lab_jack.getAIN(self.pin)
		except LabJackException, e:
			print 'LabJackException during sensor read', e
			self.valid_satus = False
		return self.latest_raw_value

class PressureSensor(LabJackSensor):
	def __init__(self, lab_jack, pin, name, offset, scale):
		""" Create a new pressure sensor.
		:param lab_jack: Lab Jack Analog to Digital converter object, see http://labjack.com/support/labjackpython.
		:type lab_jack: u3
		:param pin: The analog input pin on the LabJack which the sensor's signal is connected to.
		:type pin: integer >= 0
		:param name: The sensor's name (e.g. 'chamber pressure').
		:param offset: The sensor's raw output at atmospheric pressure [volt].
		:param scale: The sensor's voltage-to-pressure scaling [pascal volt^-1].
		"""
		self.name = name
		self.type = 'pressure'
		self.raw_units = 'volt'
		self.converted_units = 'pascal'
		self.offset = offset
		self.scale = scale
		super(PressureSensor, self).__init__(lab_jack, pin)

	def convert_raw(self, raw):
		""" Convert a raw sensor reading (i.e. volts) to physical units.
		Overrides function in Sensor.
		:param raw: Raw sensor reading [volt].
		:returns: Sensed pressure [pascal].
		"""
		pressure = (raw - self.offset) * self.scale
		# If the sensed pressure is less than vacuum, then the reading is invalid.
		# If the pressure transducers are not getting power, they will read ~0 volts and produce sub-vacuum
		# pressure readings.
		if pressure < -103e3:
			self.valid_satus = False
			print 'Warning: sub-vacuum pressure reading. Are the pressure transducers powered?'
		return pressure
class u3:
	""" Spoofs the LabJack software interface for hardware-out-of-the-loop
	(HOOTL) testing.
	"""
	
	def __init__(self):
		self.ain_values = [0]*8

	@staticmethod
	def U3():
		return u3()

	def configU3(self):
		pass

	def getCalibrationData(self):
		pass

	def configIO(self, FIOAnalog=None):
		pass

	def getAIN(self, pin):
		return self.ain_values[pin]
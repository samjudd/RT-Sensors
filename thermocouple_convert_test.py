from thermocouple_convert import ThermocoupleConverter
import numpy as np
import matplotlib.pyplot as plt

tc = ThermocoupleConverter('thermocouple_type_B.csv')

volt = np.linspace(tc.voltage.min(), tc.voltage.max(), 10000)
temp = np.zeros(volt.shape)
for i in xrange(len(volt)):
	temp[i] = tc.get_temperature(volt[i])

plt.plot(volt, temp)
plt.xlabel('Unamp. Voltage [v]')
plt.ylabel('Temperature [K]')

plt.show()

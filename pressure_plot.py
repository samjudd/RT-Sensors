import numpy as np
import sys
import os.path
from matplotlib import pyplot as plt

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print 'Usage: %s results_file.csv\n' % (sys.argv[0])

	units = 'psi'
	table_name = sys.argv[1]
	if not os.path.isfile(table_name):
		raise ValueError("No results file exists with name %s."%(table_name))
	
	M = np.genfromtxt(table_name, delimiter=",")
	p_raw = M[:, 0:2]

	interval = 0.030
	t = np.arange(0, len(p_raw[:,0])*interval, interval)

	plt.hold('on')
	for i in [0,1]:
		scale = 5000.0 / 4.0 * 0.006895
		if units == 'psi':
			scale = 5000.0 / 4.0
		offset = np.mean(p_raw[0:50, i])
		p = scale * (p_raw[:, i] - offset)
		plt.plot(t, p, label='Pressure %d' % i)

	plt.xlabel('Time [s]')
	plt.ylabel('Pressure [%s]'%units)
	plt.grid('on')
	plt.title('Pressure Trace')
	plt.show()
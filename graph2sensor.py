import u3
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import json
import random

# AIN0 - Pressure 1
# AIN1 - Pressure 2
# AIN2 - Temperature 1
# AIN3 - Load cell


def record(filename, pins=[0,1,2,3,4], t=5, freq=5000):
	# set FIO0 - FIO7 to be analog inputs corresponding to AIN0 - AIN7

	d = u3.U3()
	d.configU3()
	d.getCalibrationData()

	d.configIO(FIOAnalog=255)
	d.streamConfig(NumChannels=len(pins), PChannels = pins, Resolution=3, ScanFrequency = freq, NChannels=[31]*len(pins))
	f = open(filename, 'wb')
	d.streamStart()
	start = datetime.now()

	pin_str = ['AIN' + str(k) for k in pins]
	try:	
		for r in d.streamData():
			time = datetime.now() - start
		# print 'Got %d packets at %s' % (r['numPackets'], time.total_seconds())
			if time.total_seconds() > t:
				break
			else:
				sample = {}
				sample['time'] = time.total_seconds()
				for s in pin_str:
					sample[s] = r[s]
				f.write(json.dumps(sample))
				f.write('\n')
			print 'Pre-regulator Pressure (psi):', (r['AIN0'][0] - 1) * 1250.
			print 'Chamber Pressure (psi):', (r['AIN1'][0] - 1) * 1250.
			print 'Temp:', r['AIN2'][0]
			print 'Force (kg):', r['AIN3'][0] * 2.95
			print
	except KeyboardInterrupt:
		pass
	d.streamStop()
	d.close()
	f.close()
	return filename

def log_to_array(log_file):
	f = open(log_file)
	line = f.readline()
	f.seek(0)
	d = json.loads(line)
	pin_str = ['AIN0', 'AIN1', 'AIN2', 'AIN3']
	sample_list = [] * 5
	d_list = map(json.loads, f.readlines())
	for count in range(len(d_list)-1):
		d = d_list[count]
		next_d = d_list[count + 1]
		total_time = next_d['time'] - d['time']
		sample_count = len(d['AIN0'])
		dt = total_time / sample_count
		for count2 in range(sample_count):
			v = []
			v.append(d['time'] + count2 * dt)
			v.append((d['AIN0'][count2] - 1) * 1250.)
			v.append((d['AIN1'][count2] - 1) * 1250.)
			v.append(d['AIN2'][count2])
			v.append(d['AIN3'][count2] * 2.95)
			sample_list.append(v)
	return np.array(sample_list)


def save_array(array, filename):
	np.savetxt(filename, array, delimiter=',')

def file_to_array(csv_file):
	return np.genfromtxt(csv_file, dtype=float, delimiter=',')


def graph(array):
	# reader = csrd.v.reader(open(filename))
	# arr = np.array(list(reader))

	plt.xlabel('Time (s)')
	fig, ax1 = plt.subplots()
	ax1.set_ylabel('Pressure (psi')
	ax1.plot(arr[:,0], arr[:,1], 'r-', label='Pre-regulator Pressure(psi)')
	ax1.plot(arr[:,0], arr[:,2], 'b-', label='Chamber Pressure(psi)')
	ax1.set_ylabel('Pressure (psi')

	ax2 = ax1.twinx()
	ax2.plot(arr[:,0], arr[:,4], 'g-', label='Force(kg)')
	ax2.plot(arr[:,0], arr[:,3], 'k-', label='Temperature')
	ax2.set_ylabel('Force (kg) / Temp')
	# plt.legend(loc=2, bbox_to_anchor=(1, 0.5), borderaxespad=0.)
	plt.legend(loc='center right')
	# plt.savefig(filename.split('.')[0]+'.png', bbox_inches='tight')
	plt.show()

def integral(samples, freq, start, end):
	return sum(samples[start:end]) / freq

def plot():
	plt.ion()
	line, = plt.plot(range(100))
	# line.set_xdata([-k for k in range(100)])
	plt.ylim([0,1])
	y = [0] * 100
	while True:
		y = y[1:] + [random.random()]
		line.set_ydata(y)
		plt.draw()
		time.sleep(.01)

"""
if __name__ == '__main__':
	filename = 'output-'+str(datetime.today()).replace(':','-')+'.txt'
	record(filename, pins=[0,1,2,3], t=300.)
	print 'Test Complete. Converting file to .csv and graphing results'
	arr = log_to_array(filename)
	save_array(arr, 'cold-flow-8.csv')
	graph(arr)
"""


if __name__ == '__main__':
	plot()
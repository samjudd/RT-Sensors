import numpy as np
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import time


def f(t):
    return np.exp(-t) * np.cos(2*np.pi*t)

t1 = np.arange(0.0, 5.0, 0.1)
t2 = np.arange(0.0, 5.0, 0.02)




def update_line(num, data, line, img):
    line.set_data(data[...,:num])
    if num == 24:
        img.set_visible(True)
    return line, img


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


if __name__ == '__main__':
	fig1 = plt.figure()

	data = np.random.rand(2, 25)
	ax1=plt.subplot(411)
	l, = plt.plot([], [], 'rx')
	plt.xlim(0, 1)
	plt.ylim(0, 1)
	plt.xlabel('x')
	plt.title('test')
	ax2=plt.subplot(412)	
	nhist, xedges, yedges = np.histogram2d(data[0,:], data[1,:])
	img = plt.imshow(nhist, aspect='auto', origin='lower')
	img.set_visible(False)
	line_ani = animation.FuncAnimation(fig1, update_line, 25, 
                                   fargs=(data, l, img),
                                   interval=50, blit=True)
	line_ani.repeat = False
	plt.show()

	plt.subplot(413)
	plt.plot(t1, f(t1), 'bo', t2, f(t2), 'k')

	plt.subplot(414)
	plot()
	

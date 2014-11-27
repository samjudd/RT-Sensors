import os.path
import numpy as np
from scipy.optimize import minimize

def cost(x, F, L, S):
	""" Cost function on decision variable for optimization.
	"""
	assert(F.shape[0] == L.shape[0])
	assert(F.shape[1] == 3)
	assert(L.shape[1] == 3)
	K_1, K_0 = get_gain(x)
	c = 0
	for i in xrange(F.shape[0]):
		e = K_1.dot(L[i,:]) + K_0 - F[i,:]
		c += e.T.dot(S).dot(e)
	return c

def get_gain(x):
	""" Extract the gain matrices from the decision variable vector.
	"""
	K_1 = x[0:9].reshape((3,3))
	K_0 = x[9:12]
	return (K_1, K_0)

class LoadCellCalibrate():
	def __init__(self, table_name):
		""" Load a new load cell data table.
		The training data table should have one experiment per row. The first 3 columns
		are the applied force vector. The 4th, 5th, and 6th columns are the load cell
		readings produced by applying that force.

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
		self.F = table[1:,0:3]
		self.L = table[1:,3:6]
		self.n = self.F.shape[0]

	def solve_gain(self):
		""" Finds the gain matrices K_1, K_0 which minimize the error in the relation
		
		F_i = K_1 * L_i + K_0 
		
		where F_i is the ith applied force 3-vector from the training set and
		L_i is the ith load cell reading 3-vector from the training set.
		"""
		# Initial guess
		x_0 = np.random.rand(12)
		# Error cost matrix. Must be symmetric positive definite. Making the i,i term larger
		# increases the cost of errors on the i element of the force output.
		S = np.eye(3,3)
		res = minimize(cost, x_0, args=(self.F, self.L, S))		
		K_1, K_0 = get_gain(res.x)
		return (K_1, K_0)
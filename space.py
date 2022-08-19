import matplotlib.pyplot as plt
import numpy as np

from skfda import FDataGrid

class Space:
	'''
	pendulum state space
	g = gravitational constant
	l = length of pendulum

	STATE: [angle, angular vel]
	'''
	def pendulum2d(l: float):
		g = 9.8
		p = g / l

		return Space(
			[[ 0, 1],
			 [-p, 0]],
			[],
			[],
			[]
		)

	'''
	J: moment of inertia
	K: electromotive force and motor torque (equal)
	R: resistance
	V: rad/s/volt

	ex. dcmotor(0.01, 0.0097, 0.12, 97.4)

	STATE: [angle, angular vel]
	'''
	def dcmotor(J, K, R, V):
		return Space(
			# [[-b / J, K / J],
			#  [-K / L, -R / L]],
			# [[  0  ],
			#  [1 / L]],
			# [1, 0],
			# []
			[[0, 1],
			 [0, -K / (V * R * J)]],
			[[0],
			 [K / (R * J)]],
			[],
			[]
		)

	def __init__(self, a, b, c, d) -> None:
		self.a = a
		self.b = b
		self.c = c
		self.d = d

	def dynamics(self, x, u=None, index=None):
		out = np.add(
			np.matmul(self.a, x),
			(0 if u is None else np.matmul(self.b, u)))

		if index is None:
			return out
		
		return float(out[index][0])

	def output(self, x, u=None, index=None):
		out = np.add(
			np.matmul(self.c, x),
			(0 if u is None else np.matmul(self.d, u)))

		if index is None:
			return out
		
		return float(out[index][0])
	
	'''
	grid_points: list of axes
	'''
	def get_surface(self, grid_points: list):
		states = len(grid_points)

		data_matrix = np.zeros([states] + [len(grid_points[i]) for i in range(states)])

		for idx in np.ndindex(data_matrix.shape[1:]):
			mat = [[grid_points[i][n]] for i, n in enumerate(idx)]
			dyn = self.dynamics(mat)

			for i in range(states):
				data_matrix[tuple([i]) + idx] = dyn[i][0]

		return FDataGrid(data_matrix, grid_points)

def pendulum_phase_space():
	space = Space.pendulum2d(5)

	mesh = np.meshgrid(
		np.arange(-3, 3, 0.5),
		np.arange(-3, 3, 0.5),
	)
	u, v = [np.zeros(mesh[0].shape) for _ in range(2)]

	for idx in np.ndindex(u.shape):
			d = space.dynamics(
				[[mesh[0][idx]],
				 [mesh[1][idx]]])
			u[idx] = float(d[0][0])
			v[idx] = float(d[1][0])

	plt.quiver(*mesh, u, v)
	plt.xlabel('angle (rad)')
	plt.ylabel('vel (rad/sec)')
	plt.title('2D Pendulum Phase Space')
	plt.show()

def dcmotorsim():
	space = Space.dcmotor(0.01, 0.0097, 0.12, 97.4)

	max_time = 100
	x = np.arange(max_time)

	ang, angvel, v = [np.zeros((max_time,)) for _ in range(3)]

	voltage = [[10]]
	state = [[0], [0]]

	for i in x:
		ang[i] = state[0][0] / 1000
		angvel[i] = state[1][0] / 50
		v[i] = voltage[0][0]

		if i == 50:
			voltage[0][0] = 0

		state = np.add(state, space.dynamics(state, u=voltage))

	ax = plt.subplots()[1]

	ax.plot(x, ang, color='g', label='Angle (1000 rads)')
	ax.plot(x, angvel, color='b', label='Angular Velocity (50 rads/s)')
	ax.plot(x, v, color='r', label='Voltage')
	ax.legend(loc='upper left')
	ax.set_title('Simulated DC Motor')
	plt.show()

if __name__ == '__main__':
	dcmotorsim()

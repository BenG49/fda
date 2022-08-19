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
			np.identity(2),
			np.identity(2),
			np.identity(2)
		)

	'''
	J: moment of inertia
	K: electromotive force and motor torque (equal)
	R: resistance
	V: rad/s/volt

	STATE: [angle, angular vel]
	'''
	def dcmotor(J, K, R, V):
		return Space(
			[[0, 1],
			 [0, -K / (V * R * J)]],
			[[0],
			 [K / (R * J)]],
			[0, 1],
			np.identity(2)
		)
	def dcmotor_default():
		return Space.dcmotor(0.01, 0.0097, 0.12, 97.4)

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
	def get_data(self, state_axes: list, input_axes: list):
		states = len(state_axes)
		inputs = len(input_axes)

		# get number of output states
		outstates = self.output([0]*states)
		outstates = 1 if type(outstates) is not int else len(outstates)

		data_matrix = np.zeros([outstates] + [len(s) for s in state_axes] + [len(i) for i in input_axes])

		for idx in np.ndindex(data_matrix.shape[1:]):
			x = [state_axes[i][idx[i]] for i in range(states)]

			u = None
			if inputs > 0:
				u = [input_axes[i - states][idx[i]] for i in range(states, states + inputs)]

			out = self.output(self.dynamics(x, u))
			print(f'{x} + {u if u is not None else ""} -> {self.dynamics(x, u)}')

			if outstates == 1:
				data_matrix[tuple([0]) + idx] = out
			else:
				for i in range(states):
					data_matrix[tuple([i]) + idx] = out[i]

		real_shape = [d for d in data_matrix.shape if d > 1]
		real_axes = [d for d in state_axes + input_axes if len(d) > 1]
		
		return FDataGrid([data_matrix.reshape(real_shape)], real_axes)

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
	space = Space.dcmotor_default()

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

import matplotlib.pyplot as plt
import numpy as np


class Space:
	# pendulum state space
	# g = gravitational constant
	# l = length of pendulum

	# STATE: [angle, angular vel]
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


	def __init__(self, a, b, c, d) -> None:
		self.a = np.matrix(a)
		self.b = np.matrix(b)
		self.c = np.matrix(c)
		self.d = np.matrix(d)

	def dynamics(self, x, u=None):
		print(float((self.a * x)[1][0]))
		return self.a * x + (0 if u is None else self.b * u)

	def output(self, x, u=None):
		return self.c * x + (0 if u is None else self.d * u)

if __name__ == '__main__':
	p = Space.pendulum2d(5)

	angle, vel = np.meshgrid(
		np.arange(-3, 3, 0.5),
		np.arange(-3, 3, 0.5),
	)
	u, v = [], []

	for i in range(len(angle)):
		u.append([])
		v.append([])

		for j in range(len(angle[i])):
			d = p.dynamics(np.matrix([[angle[i][j]], [vel[i][j]]]))
			u[i].append(float(d[0][0]))
			v[i].append(float(d[1][0]))

	plt.quiver(angle, vel, u, v)
	plt.xlabel('angle (rad)')
	plt.ylabel('vel (rad/sec)')
	plt.title('2D Pendulum Phase Space')
	plt.show()

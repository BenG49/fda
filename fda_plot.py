# import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from skfda import FDataGrid
from skfda.representation import basis
from space import Space

import util

BSPLINE, FOURIER, MONOMIAL, TENSOR, VECTORVALUED = range(5)

basis_titles = {
	BSPLINE: 'BSpline',
	FOURIER: 'Fourier',
	MONOMIAL: 'Monomial',
	TENSOR: 'Tensor',
	VECTORVALUED: 'Vector Valued',
}

def make_simple_basis(b, n):
	if b == BSPLINE:
		return basis.BSpline(n_basis=n, order=min(4, n))
	elif b == FOURIER:
		return basis.Fourier(n_basis=n)
	elif b == MONOMIAL:
		return basis.Monomial(n_basis=n)
	else:
		raise ValueError('Invalid basis function type')	

def test_covid_data(bases: list, max_basis: int, min_basis: int=1):
	fd = util.read_fdatagrid('us.csv')
	fd.plot()

	cols = max_basis - min_basis + 1
	y_ticks = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x / 10000))
	fig, ax = plt.subplots(nrows=len(bases), ncols=cols)

	for y, b in enumerate(bases):
		for n in range(min_basis, max_basis + 1):
			if len(bases) == 1:
				a = ax[n - min_basis]
			else:
				a = ax[y, n - min_basis]
			
			a.yaxis.set_major_formatter(y_ticks)
			a.set_ylabel('10,000 cases')
			a.set_title(f'{basis_titles[b]} n={n}')
			fig = fd.to_basis(make_simple_basis(b, n)).plot(axes=a)

	fig.tight_layout()
	plt.show()

def pendulum_fda():
	fig = plt.figure()
	ax = fig.gca(projection='3d')

	l = Space.pendulum2d(5).get_surface(
		grid_points = [
			np.arange(-3, 3, 0.5),
			np.arange(-3, 3, 0.5)
		])
	l.plot(axes=ax)

	l.to_basis(
		basis.Tensor([
			basis.Fourier(n_basis=4, domain_range=l.domain_range[0]),
			basis.Fourier(n_basis=4, domain_range=l.domain_range[1])
		])
	).plot(axes=ax)

	ax.set_xlabel('angle (rad)')
	ax.set_ylabel('velocity (rad/s)')
	ax.set_zlabel('change')
	plt.show()

pendulum_fda()
# test([BSPLINE, MONOMIAL, FOURIER], min_basis=6, max_basis=8)

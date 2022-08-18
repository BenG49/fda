import numpy as np
from sklearn.linear_model import LinearRegression

class Series:
	def __init__(self, time_start, time_end, data=None, func=None, vals=None):		
		if data is not None:
			self.data = data
		elif func is not None:
			if vals is None:
				raise ValueError('Must provide count of times if providing function')

			self.data = np.zeros(vals)
			
			t = time_start
			delta = (time_end - time_start) / vals
			for i in range(vals):
				t += delta
				self.data[i] = func(t)
		else:
			raise ValueError('Must provide either data or function to generate data')

		
		self.time_delta = (time_end - time_start) / len(self.data)

		self.times = np.linspace(time_start, time_end, len(self.data))

	def plot(self, ax, **kwargs):
		ax.plot(self.times, self.data, **kwargs)

	def get(self, t):
		i = int((t - self.times[0]) // self.time_delta)
		return self.data[i]

def naive(series, horizon):
	start = series.times[-1]
	n = int(horizon // series.time_delta)

	return Series(
		start,
		start + horizon,
		[series.data[-1]] * n)

def seasonal_naive(series, horizon):
	start = series.times[-1]
	n = int(horizon // series.time_delta)

	return Series(
		start,
		start + horizon,
		func=lambda t: series.get(t - 365),
		vals=n)

def linreg(series, horizon):
	start = series.times[-1]
	n = int(horizon // series.time_delta)

	x = np.array(series.times).reshape((-1, 1))
	y = np.array(series.data).reshape((-1, 1))

	model = LinearRegression().fit(x, y)

	reg = Series(
		start,
		start + horizon,
		func=lambda t: model.predict([[t]]),
		vals=n)

	return reg

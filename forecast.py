class Series:
	def __init__(self, time_start, time_end, data=None, func=None, vals=None):		
		if data is not None:
			self.data = data
		elif func is not None:
			if vals is None:
				raise ValueError('Must provide count of times if providing function')

			self.data = [0] * vals
			
			t = time_start
			delta = (time_end - time_start) / vals
			for i in range(vals):
				t += delta
				self.data[i] = func(t)
		else:
			raise ValueError('Must provide either data or function to generate data')

		
		self.time_delta = (time_end - time_start) / len(self.data)

		self.times = [time_start + self.time_delta * i for i in range(len(self.data))]

	def plot(self, ax, c=None, label=None, linestyle=None):
		ax.plot(self.times, self.data, c=c, label=label, linestyle=linestyle)

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

	return Series(
		start,
		start + horizon,
		func=lambda t: series.get(t - 365),
		vals=len(series.data))

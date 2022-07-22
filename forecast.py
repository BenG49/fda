class Series:
	def __init__(self, time_start, time_end, data):
		diff = time_end - time_start
		self.time_delta = diff / len(data)

		self.times = [time_start + self.time_delta * i for i in range(len(data))]
		self.data = data

	def plot(self, ax, c=None, label=None, linestyle=None):
		ax.plot(self.times, self.data, c=c, label=label, linestyle=linestyle)

def naive(series, horizon):
	start = series.times[-1]

	n = int(horizon.total_seconds() // series.time_delta.total_seconds())

	return Series(
		start,
		start + horizon,
		[series.data[-1]] * n)

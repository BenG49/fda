import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from datetime import datetime, timedelta

import forecast

data = pd.read_csv('us.csv').to_numpy()

deltas = [0] * len(data)
for i in range(1, len(data)):
	deltas[i] = data[i, 1] - data[i - 1, 1]

data = np.insert(data, 2, deltas, axis=1)

for i in range(len(data[:, 0])):
	data[i, 0] = datetime.strptime(data[i, 0], '%Y-%m-%d')

FIRST_TIME = data[0, 0]
LAST_TIME = data[-1, 0]

### PLOT ###

fig, ax = plt.subplots()

ax.xaxis.set_major_locator(ticker.MultipleLocator(60))
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))

cases = forecast.Series(0, len(data), data[:, 1])
newcases = forecast.Series(0, len(data), data[:, 2])
naive = forecast.naive(newcases, 100)
seasonal = forecast.seasonal_naive(newcases, 100)

# cases.plot(ax, c='b', label='Total Cases')
newcases.plot(ax, c='g', label='New Cases')
# naive.plot(ax, label='Naive', linestyle='--')
seasonal.plot(ax, label='Seasonal Naive', linestyle='--')
ax.legend(loc=2)

plt.xticks(rotation=45)
plt.gcf().subplots_adjust(bottom=0.2)
plt.title('Covid-19 total cases')
plt.show()

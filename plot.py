import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import forecast
import util

data = util.read_data('us.csv')

FIRST_TIME = data[0, 0]
LAST_TIME = data[-1, 0]
HORIZON = 200

### PLOT ###

fig, ax = plt.subplots()

ax.xaxis.set_major_locator(ticker.MultipleLocator(60))
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x / 10000)))
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))

cases = forecast.Series(0, len(data), data[:, 1])
newcases = forecast.Series(0, len(data), data[:, 2])
naive = forecast.naive(newcases, HORIZON)
seasonal = forecast.seasonal_naive(newcases, HORIZON)
linreg = forecast.linreg(newcases, HORIZON)

# cases.plot(ax, c='b', label='Total Cases')
newcases.plot(ax, c='g', label='New Cases')
naive.plot(ax, label='Naive', linestyle='--')
seasonal.plot(ax, label='Seasonal Naive', linestyle='--')
linreg.plot(ax, label='Linear Regression', linestyle='--')

ax.set_ylabel('10,000 cases')
ax.set_xlabel('days')
ax.legend(loc=2)

plt.xticks(rotation=45)
plt.gcf().subplots_adjust(bottom=0.2)
plt.title('Covid-19 new cases')
plt.show()

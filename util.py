import pandas as pd
import numpy as np
from datetime import datetime
from skfda import FDataGrid

def read_data(file: str):
	data = pd.read_csv(file).to_numpy()

	deltas = [0] * len(data)
	for i in range(1, len(data)):
		deltas[i] = data[i, 1] - data[i - 1, 1]

	data = np.insert(data, 2, deltas, axis=1)

	for i in range(len(data[:, 0])):
		data[i, 0] = datetime.strptime(data[i, 0], '%Y-%m-%d')

	return data

def read_fdatagrid(file: str, newcases=True) -> FDataGrid:
	data = read_data(file)

	return FDataGrid(
		data_matrix=list(data[:, (2 if newcases else 1)]),
		grid_points=np.linspace(0, len(data) - 1, len(data))
	)

import pandas as pd
import numpy as np
import json
from matplotlib import pyplot as plt
from datetime import datetime

# def load_live():
# 	try:
# 		data = pd.read_csv('live.csv')
# 	except OSError as e:
# 		## if we have not create such file
# 		with open("live.csv",'w') as f:
# 			pass # just create it without edited
# 		data = pd.DataFrame() # create a empty pd.DataFrame.
# 	return data

def init_plot():
	plt.style.available
    # seaborn.set_style("darkgrid")
	plt.rc("figure", figsize=(12, 8))
	plt.rc("savefig", dpi=90)
	plt.rc("font", family="sans-serif")
	plt.rc("font", size=14)
	plt.style.use('ggplot')


if __name__ == '__main__':
	##  load the data
	DATA = pd.read_json("result.json")

	## Sepread the Sec and seat from Seat
	DATA[['Section','Seat']] = DATA['Seat'].str.split(', ',expand = True)
	dd = pd.DataFrame()
	dd = DATA['Section'].str.split(expand = True).iloc[:,1] # get only the section number
	DATA['Section'] = dd
	DATA['Section'] = DATA['Section'].astype(int) # convert the section into int64 type
	DATA['Price'] = DATA['Price'].replace('[\$,]', '', regex=True).astype(float) # convert the price into float64 type
	DATA = DATA[['Section','Seat','Price']] # and re-ordering,

	## filter out those 'bad' seat.
	DATA = DATA.loc[DATA['Section'] < 100] # just want those section that within 100.
	
	## Customs matplot
	init_plot()

	## load live_data
	# live_result = load_live() # it is a pandas DataFrame obj.

	## update live chat dataset
	col_name = pd.to_datetime(datetime.now()) # set the new colname with now() time
	# create and update a new column with now() time as col's name
	# live_result[Col_name] = (DATA['Price'].groupby(DATA['Section']).min())

	## plot()
	pp = DATA.boxplot(by = 'Section')
	pp.set_title("Ticket Price Distribution")
	pp.set_ylim([200,800])
	plt.show()





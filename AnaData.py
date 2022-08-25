import pandas as pd
import numpy as np
import json
from matplotlib import pyplot as plt
from datetime import datetime


def init_plot():
    plt.style.available
    # seaborn.set_style("darkgrid")
    plt.rc("figure", figsize=(12, 8))
    plt.rc("savefig", dpi=90)
    plt.rc("font", family="sans-serif")
    plt.rc("font", size=14)
    plt.style.use('ggplot')

def data_clean():
    DATA = pd.read_json("result.json")

    data = DATA[:]
    dd = data['Seat'].str.split(', ' , expand = True).iloc[:,0]
    dd = dd.str.split(expand = True).iloc[:,1]
    data['Section'] = dd
    data['Section'] = data['Section'].astype(int)
    data['Price']= data['Price'].replace('[\$,]', '', regex=True).astype(float)

    # filter out those 'bad' seat.
    # just want those section that within 100.
    data = data.loc[data['Section'] < 100]

    return data[['Section','Seat','Price']]

if __name__ == '__main__':
    # load the data
    data = data_clean()

    init_plot()

    # plot
    pp = data.boxplot(by='Section')
    pp.set_title("Ticket Price Distribution")
    pp.set_ylim([200, 800])
    plt.show()


    '''
    # Sepread the Sec and seat from Seat
    data = DATA['Seat'].str.split(', ', expand=True)
    dd = pd.DataFrame()
    # get only the section number
    dd = DATA['Section'].str.split(expand=True).iloc[:, 1]
    DATA['Section'] = dd
    DATA['Section'] = DATA['Section'].astype(
        int)  # convert the section into int64 type
    DATA['Price'] = DATA['Price'].replace('[\$,]', '', regex=True).astype(
        float)  # convert the price into float64 type
    DATA = DATA[['Section', 'Seat', 'Price']]  # and re-ordering,



    # load live_data
    # live_result = load_live() # it is a pandas DataFrame obj.

    # update live chat dataset
    # set the new colname with now() time
    col_name = pd.to_datetime(datetime.now())
    # create and update a new column with now() time as col's name
    # live_result[Col_name] = (DATA['Price'].groupby(DATA['Section']).min())

    # plot()

    '''

from re import X
from django.shortcuts import render
import mysql.connector
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from .utils import get_plot


def day_django(x, y):
    engine = create_engine('mysql+mysqlconnector://root:password@localhost:3306/NeuraData')
    period = pd.read_sql("SELECT * FROM vsumperiodvaluesday_django", engine)
    df = pd.DataFrame(period, columns=['DateOnly','EnergyCost'])
    my_dictionary = {}
    x = []
    y = []
    for column in df:
        columnSeriesObj = df[column]
        if column == 'DateOnly':
            x = columnSeriesObj.values
        elif column == 'EnergyCost':
            y = columnSeriesObj.values
        my_dictionary[column] = [x,y]
        print(my_dictionary)
    #chart = get_plot(x,y)
    #if x == 1:
    df.plot(x ='DateOnly', y='EnergyCost', kind = 'line')
    plt.show()





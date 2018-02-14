__author__ = 'amendrashrestha'

# date_input = "2017/11/02"
# from datetime import datetime
# # date_input = '15 november, 2014 17:16'
# date_object = datetime.strptime(date_input, '%Y/%m/%d')
# print(date_object.strftime('%Y-%m-%d'))

# tmp_date = '15 november, 2014 • 17:16 1 Comment '
#
# date = tmp_date.replace("• ", "").split(' ')[:-2]
# print(' '.join(date))



import plotly.plotly as py
import plotly.graph_objs as go

# Create random data with numpy
import numpy as np

N = 500
random_x = np.linspace(0, 1, N)
random_y = np.random.randn(N)

# Create a trace
trace = go.Scatter(
    x = random_x,
    y = random_y
)

data = [trace]

py.iplot(data, filename='basic-line')
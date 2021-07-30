#!/usr/bin/env python
#
# plotter for mri cluster pdu power
#
#format of pdupower-YYYYMMDD
#1538595061,u22,10.90,363,417,310
# epochtime,rack,pdu1,pdu2,pdu3
# pdu units in 10W
#
# too big for online as of 2019-09-20
#
#from plotly.offline import plot # following for online rather than offline
import glob
import os
import time
import pandas as pd
# deprecated
#import plotly.plotly as py
# did this go away?
import chart_studio.plotly as py
import plotly.graph_objs as go
import plotly.io as pio
#import chart_studio.graph_objs as go

from datetime import datetime
import pytz

py.plotly.tools.set_credentials_file(username='jonesm', api_key='f91fad0x9z')
#x = [
#    datetime(year=2013, month=10, day=04),
#    datetime(year=2013, month=11, day=05),
#    datetime(year=2013, month=12, day=06)
#]

#data = [
#    go.Scatter(
#        x=x,
#        y=[1, 3, 6]
#    )
#]
#plot(data, filename='python-datetime')

tz = pytz.timezone('America/New_York')

rack_load = dict() # key = rack, value = load in kW
rack_time = dict()
rack_time2 = dict()
rack_load2 = dict()

LOGDIR = "/srv/cosmos/logging/pdupower"
# this parsing is really slow, try pandas to see if it speeds up?
for infilename in sorted(glob.glob("/srv/cosmos/logging/pdudata/pdupower-2021072*"), key=os.path.getmtime):
    t0 = time.time()
    with open(infilename) as infile:
        allrecords = infile.readlines()[:] # no header
	# sam's log format is:
	# time,rack,kW
        for line in allrecords:
            line_words = line.split(',')
            #print 'line_words[0] = ',line_words[0]
            # epoch time is first, convert
            dt = datetime.fromtimestamp(float(line_words[0]), tz)
            date_string = dt.strftime('%Y-%m-%dT%H:%M:%S')
            rack = line_words[1]
            load = float(line_words[2])
            rack_load[rack] = rack_load.get(rack, []) + [load]
            rack_time[rack] = rack_time.get(rack, []) + [date_string]

    t1=time.time()
    print("0. %f secs for file %s" % (t1-t0,infilename))

    # pandas version only about 10% faster
    #t2 = time.time()
    #df = pd.read_csv(infilename,header=None)
    #for row in zip(df[0],df[1],df[2]):
    #    dt = datetime.fromtimestamp(float(row[0]), tz)
    #    date_string = dt.strftime('%Y-%m-%dT%H:%M:%S')
    #    rack = row[1]
    #    load = float(row[2])
    #    rack_load2[rack] = rack_load2.get(rack, []) + [load]
    #    rack_time2[rack] = rack_time2.get(rack, []) + [date_string]
#
    #t3 = time.time()
    #print("1. %f secs for file %s" % (t3-t2,infilename))

#print(rack_time["h22"],rack_load["h22"])
trace1 = go.Scattergl(
    x=rack_time["h22"],
    y=rack_load["h22"],
    name='Rack h22',
    mode='lines+markers'
)
trace2 = go.Scattergl(
    x=rack_time["h23"],
    y=rack_load["h23"],
    name='Rack h23',
    mode='lines+markers'
)
trace3 = go.Scattergl(
    x=rack_time["h24"],
    y=rack_load["h24"],
    name='Rack h24',
    mode='lines+markers'
)
trace4 = go.Scattergl(
    x=rack_time["h25"],
    y=rack_load["h25"],
    name='Rack h25',
    mode='lines+markers'
)
	
# output csv

#data = go.Scatter([trace1,trace2,trace3,trace4,trace5,trace6,trace7,trace8,trace9,trace10,trace11,trace12])
#data = [trace1,trace2,trace3,trace4,trace5,trace6,trace7,trace8,trace9,trace10,trace11,trace12,trace13,trace14,trace15,trace16]
data = [trace1,trace2,trace3,trace4]
#print(data)
layout = go.Layout(title="Industry cluster power",xaxis={'title':'datetime'},yaxis={'title':'kW'})
figure = go.Figure(data=data,layout=layout)
#data = [trace1,trace2,trace3,trace4]
#plot(data,filename='python-login') # offline version
# online version
#py.plot(figure,filename='ind-power',auto_open=False)
# offline version - fixed
pio.write_html(figure,file='index.html',auto_open=False)
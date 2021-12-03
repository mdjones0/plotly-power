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
import gc
import csv

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

#
# size of dicts, we get one value per rack per min, or 1440 per day,
#  525600 per 365d
rack_load = {new_list: [] for new_list in ("m22","h22","h23","h24","h25", \
	"p22","p23","p24","p25","p26","p27","p28", \
	"q06","q07","q08","q09", \
	"u22","u23","u24","u25","u26","u27","u28", \
	"v05","v07","v09","v10","v11")} # key = rack, value = load in kW
rack_time = {new_list: [] for new_list in ("m22","h22","h23","h24","h25", \
	"p22","p23","p24","p25","p26","p27","p28", \
	"q06","q07","q08","q09", \
	"u22","u23","u24","u25","u26","u27","u28", \
	"v05","v07","v09","v10","v11")}
#rack_time = dict()
#rack_load = dict()
#rack_time2 = dict()
#rack_load2 = dict()

LOGDIR = "/srv/cosmos/logging/pdupower"
# this parsing is really slow, try pandas to see if it speeds up?
# https://stackoverflow.com/questions/2473783/is-there-a-way-to-circumvent-python-list-append-becoming-progressively-slower
# turning gc off does not seem to help
#gc.disable()
#  pre-defining lists really helped, now constant per file
for infilename in sorted(glob.glob("/srv/cosmos/logging/pdudata/pdupower-202107*"), key=os.path.getmtime) + \
	sorted(glob.glob("/srv/cosmos/logging/pdudata/pdupower-20210[8-9]*"), key=os.path.getmtime) + \
	sorted(glob.glob("/srv/cosmos/logging/pdudata/pdupower-20211[0-2]*"), key=os.path.getmtime):
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
            rack_load[rack].append(load)
            rack_time[rack].append(date_string)

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

#gc.enable()
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
	
# output csv - don't need to do this often
#csvfile = open("indpower.csv","w")
#writer = csv.writer(csvfile, delimiter=",",quotechar='"',quoting=csv.QUOTE_NONNUMERIC)
#dicts = rack_time["h22"],rack_load["h22"],rack_time["h23"],rack_load["h23"],rack_time["h24"],rack_load["h24"],rack_time["h25"],rack_load["h25"]
#writer.writerow(['h22 time','h22 power','h23 time','h23 power','h24 time','h24 power','h25 time','h25 power'])
#for timeid in rack_time["h22"]:
#    writer.writerow(d[timeid] for d in dicts)

#data = go.Scatter([trace1,trace2,trace3,trace4,trace5,trace6,trace7,trace8,trace9,trace10,trace11,trace12])
#data = [trace1,trace2,trace3,trace4,trace5,trace6,trace7,trace8,trace9,trace10,trace11,trace12,trace13,trace14,trace15,trace16]
data = [trace1,trace2,trace3,trace4]
#data = [trace1]
#print(data)
layout = go.Layout(title="Industry cluster power",xaxis={'title':'datetime'},yaxis={'title':'kW'})
figure = go.Figure(data=data,layout=layout)
#data = [trace1,trace2,trace3,trace4]
#plot(data,filename='python-login') # offline version
# online version
#py.plot(figure,filename='ind-power',auto_open=False)
# offline version - fixed
pio.write_html(figure,file='index.html',auto_open=False)

#!/usr/bin/python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By : Oliver Moore
# version = '1.0'
# ---------------------------------------------------------------------------
""" 
Using PyVisa (Python wrapper for VISA - Virtual Instrument Software 
Architecture) to interface with Spectrum Analyzer over USB. A csv writer object 
is used to write the formatted time-stamped frequency (Hz) and amplitude (dB) 
data into .csv file. File is created with max permissions (RWX all users) and 
filename checked for uniqueness, otherwise user will be prompted to enter new 
filename.
"""
# ---------------------------------------------------------------------------
import pyvisa
import time
import datetime
import os
from os import path
import csv

## Check if filename exists, otherwise request user input
def check_file(filepath):
    if path.exists(filepath):
        while True:
            test_number = input("Enter Test Number\n") 
            filename = "FreqTest_" + test_number + ".csv"
            filepath = os.path.join(dirname, filename)
            newpath = filepath
            if path.exists(newpath):
                pass
            else:
                return newpath
    return filepath

## Default file "../FreqTest_1.csv" located in current working directory
filename = "FreqTest_1.csv"
dirname = os.path.dirname(__file__)
filepath = os.path.join(dirname, filename)

## Check if file already exists
filepath = check_file(filepath)

## Initialize CSV (exclusive creation, failing if file exists)
with open(filepath, mode='x', newline='', encoding='utf-8') as csvfile:
    #creating csv writer object
    csvwriter = csv.writer(csvfile, dialect='excel')
    #print header row
    csvwriter.writerow(["Date/Time", "Frequency (Hz)", "Amplitude (dBm)"])

## Set permissions of file to max (octal 777) (R/W/X for all users)
os.chmod(filepath, 0o777)

## Replace with resourceID of instrument: NI MAX or by rm.list_resources()
rm = pyvisa.ResourceManager()
inst = rm.open_resource('USB0::0xF4EC::0x1300::T0104C18460034::INSTR') 

data_List = []
arr = ()
counter = 0 

## Output date, timestamp and formatted data to csv
while True:
    data_List = [] # clear contents
    
    if(int(inst.query('*OPC?')) == 1):
        # Date and timestamp
        t = datetime.datetime.now()
        s = t.strftime('%Y-%m-%d %H:%M:%S.%f')
        head = s[:-7] # everything before the '.'
        tail = s[-7:] # including '.' and the float after
        f = float(tail)
        temp = "{:.03f}".format(f)
        new_tail = temp[1:] # ignore temp[0] since its always '0'
        current_time = head + new_tail
        data_List.append(current_time)
        
        # Retrieve and format data into list
        arr = inst.query("CALCulate:PEAK:TABLe?")
        arr = arr.strip()
        arr = arr.split(",")
        data_List.append(arr[0])
        data_List.append(arr[1].strip(';'))
        
    # Print for debugging purposes
    print(current_time + " | " + "Frequency (Hz): " + (arr[0]) + " | " + 
          "Amplitude (dB): " + (arr[1])) 
    
    # Append data to csv file (writes the differences)
    with open(filepath, 'a+', newline='', encoding='utf-8') as csvfile:
        #creating csv writer object
        csvwriter = csv.writer(csvfile, dialect='excel')
        #print row of csv data
        csvwriter.writerow(data_List)
        counter += 1
        time.sleep(1)
        
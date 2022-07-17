#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Oliver Moore
# version = '1.0'
# ---------------------------------------------------------------------------
""" Python test app for the retrieval and storage of DAQ analog sensor data.
    Using DATAQ Instruments DI-4718B DAQ with DI-8B41-02 +/-5V amplifier 
    modules to read analog sensor data from SM9236 differential pressure 
    sensor, FS4000 mass flow sensor, and E18-D80NK IR proximity sensor. Test 
    app expects user keypress to start, stop, reset, and exit. Timestamped 
    analog sensor data is stored in .csv format and user-prompted filename 
    will be checked for uniqueness, to avoid overwriting existing saved data.
    WinDAQ software can be used to view and verify the data directly from DAQ.
    
Hardware:
    - DATAQ Instruments DI-4718B 8-channel Ethernet Data Logger and Data 
      Acquisition System for DI-8B Amplifiers.
    - (x3) DI-8B41-02 Isolated ±5V 1kHz bandwidth 8B-style Amplifier modules
    - SM9236 Differential Pressure Sensor (Analog 0-5V)
    - FS4000 Mass Flow Sensor (Analog 0-5V)
    - E18-D80NK Infrared Proximity Sensor (Analog 0-5V)
    
Software:
    WinDAQ Recording and Playback Software (free) (optional)
"""

"""
COPYRIGHT © 2018 BY DATAQ INSTRUMENTS, INC.

!!!!!!!!    VERY IMPORTANT    !!!!!!!!
!!!!!!!!    READ THIS FIRST   !!!!!!!!

This program works only with the following models:
DI-1120, -2108, -4108, -4208, AND -4718B
Any other instrument model should be disconnected from the PC
to prevent the program from detecting a device with a DATAQ
Instruments VID and attempting to use it.
Such attempts will fail.

You'll need to uncomment the appropriate

slist
analog_ranges

tuples for the instrument model you will use with this program.
Prototypes are provided for each supported model, so it's a
simple matter of commenting the ones that don't apply, and
uncommenting the one that does. In its as-delivered state
the program assumes that model DI-2108 is connected.

Instruments used with this program MUST be placed in their
CDC communication mode.
Follow this link for guidance:
https://www.dataq.com/blog/data-acquisition/usb-daq-products-support-libusb-cdc/

Any specific instrument's protocol document can be downloaded from the instrument's
product page: Once there, click the DETAILS tab.
"""

import serial
import serial.tools.list_ports
import keyboard
import time
import datetime
import csv
import math

dataList_prev = [0,0,0] # List of prev analog channel data for csv file
dataList_curr = []      # List of current analog channel data for csv file
dataList_ref = []
dataList_newcurr = []   # List of the difference between prev and current data

# Copy or clone a list with slice operator
# def Cloning(li1):
#     li_copy = li1[:]
#     return li_copy


# go to: Tools -> Preferences -> Current Working Directory -> Startup -> Select the following directory
# Add directory to save the csv files

"""
Uncomment the slist tuple depending upon the hardware model you're using.
You can modify the example tuples to change the measurement configuration
as needed. Refer to the instrument's protocol for details. Note that
only one slist tuple can be enabled at a time.
"""

"""
slist for models DI-1120 and DI-4208
0x0300 = Analog channel 0, Â±10 V range
0x0401 = Analog channel 1, Â±5 V range
0x0709 = Rate input, 0-500 Hz range
0x000A = Counter input
"""
#slist = [0x0300,0x0401,0x0709,0x000A]

"""
slist for model DI-4108
0x0000 = Analog channel 0, Â±10 V range
0x0101 = Analog channel 1, Â±5 V range
0x0709 = Rate input, 0-500 Hz range
0x000A = Counter input
"""
#slist = [0x0000,0x0101,0x0709,0x000A]

"""
slist for model DI-2108
0x0000 = Analog channel 0, Â±10 V range
0x0001 = Analog channel 1, Â±10 V range
0x0709 = Rate input, 0-500 Hz range
0x000A = Counter input
"""
#slist = [0x0000,0x0001,0x0709,0x000A]

"""
slist for model DI-4718B (untested, but should work)
0x0000 = Analog channel 0, Â±5 V range
0x0001 = Analog channel 1, Â±5 V range
0x0002 = Analog channel 2, Â±5 V range
0x0003 = Analog channel 3, Â±5 V range
0x0004 = Analog channel 4, Â±5 V range
0x0709 = Rate input, 0-500 Hz range
0x000A = Counter input
"""
#slist = [0x0000,0x0001,0x0002,0x0003,0x0004,0x0709,0x000A]
slist = [0x0000,0x0001,0x0002]

"""
Uncomment an analog_ranges tuple depending upon the hardware model you're using.
Note that only one can be enabled at a time.
The first item in the tuple is the lowest gain code (e.g. Â±100 V range = gain code 0)
for the DI-4208. Some instrument models do not support programmable gain, so
their tuples contain only one value (e.g. model DI-2108.)
"""
# Analog ranges for models DI-4208 and -1120
#analog_ranges = tuple((100,50,20,10,5,2))

# Analog ranges for model DI-4108
#analog_ranges = tuple((10,5,2,1,0.5,0.2))

# Analog ranges for model DI-2108 (fixed Â±10 V measurement range)
#analog_ranges = [10]

# Analog ranges for model DI-4718B (fixed Â±5 V measurement range)
analog_ranges = [5]

"""
Define a tuple that contains an ordered list of rate measurement ranges supported by the hardware.
The first item in the list is the lowest gain code (e.g. 50 kHz range = gain code 1).
"""
rate_ranges = tuple((50000,20000,10000,5000,2000,1000,500,200,100,50,20,10,1))

# This is a list of analog and rate ranges to apply in slist order
range_table = list(())

ser = serial.Serial()

# Define flag to indicate if acquiring is active
acquiring = False

""" 
Discover DATAQ Instruments devices and models.  Note that if multiple devices are connected, only the
device discovered first is used. We leave it to you to ensure that it's the desired device model.
"""
def discovery():
    # Get a list of active com ports to scan for possible DATAQ Instruments devices
    available_ports = list(serial.tools.list_ports.comports())
    
    # Holds the com port of the detected device, if any
    hooked_port = ""
    for p in available_ports:
        if ("VID:PID=0683" in p.hwid):
            # Yes!  Dectect and assign the hooked com port
            hooked_port = p.device
            break

    if hooked_port:
        print("Found a DATAQ Instruments device on", hooked_port)
        ser.timeout = 0
        ser.port = hooked_port
        ser.baudrate = '115200'
        ser.open()
        return True
    
    else:
        print("Please connect a DATAQ Instruments device.")
        input("Press ENTER to try again...")
        return False

# Send a user command string with appended carriage return <cr>
def send_cmd(command):
    ser.write((command + '\r').encode())
    time.sleep(0.1)
    if not(acquiring):
        # Echo commands if not acquiring
        while True:
            if (ser.inWaiting() > 0):
                while True:
                    try:
                        s = ser.readline().decode()
                        s = s.strip('\n')
                        s = s.strip('\r')
                        s = s.strip(chr(0))
                        break
                    except:
                        continue
                    
                if (s != ""):
                    print(s)
                    break

# Configure the instrument's scan list
def config_scn_lst():
    # Scan list position must start with 0 and increment sequentially
    position = 0
    
    for item in slist:
        send_cmd("slist " + str(position) + " " + str(item))
        position += 1
        
        # Update the Range table
        if (((item) & (0xf)) < 8):
            # This is an analog channel. Refer to the slist prototype for your instrument
            # as defined in the instrument protocol.
            range_table.append(analog_ranges[item >> 8])

        elif (((item) & (0xf)) == 8):
            # This is a digital channel. No measurement range support.
            # Update range_table with any value to keep it aligned.
            range_table.append(0)

        elif (((item) & (0xf)) == 9):
            # This is a rate channel
            # Rate ranges begin with 1, so subtract 1 to maintain zero-based index
            # in the rate_ranges tuple
            range_table.append(rate_ranges[(item >> 8) - 1])

        else:
            # This is a count channel. No measurement range support.
            # Update range_table with any value to keep it aligned.
            range_table.append(0)


while discovery() == False:
    discovery()
    
# Stop in case Device was left running
send_cmd("stop")

# Define binary output mode
send_cmd("encode 0")
send_cmd("filter * 1")

# Configure the instrument's scan list
config_scn_lst()

# Define sample rate = 10 Hz:
# 60,000,000/(srate * dec) = 60,000,000/(11718 * 512) = 10 Hz
# send_cmd("dec 512")
# send_cmd("117180")
send_cmd("dec 500")
send_cmd("srate 1875")
send_cmd("deca 64")

# Keep the packet size small for responsiveness
send_cmd("ps 0")

print("")
print("Ready to acquire...")
print("")
print("Press <g> to go, <s> to stop, <r> to reset counter, and <q> to quit:")

# slist position pointer range: 0 (first position) to len(slist)
slist_pointer = 0
cycle_count = 0

# label = "[P1,F1,L1]"

# If filename already exists, truncate file to zero length (delete contents) 
# with 'w' flag before generating a new header row
serial_number = input("Enter Serial Number\n")
trial_number = input("Enter Trial Number. Ex. 001,002,..\n")
filename = "Test_" + serial_number + "_" + trial_number + ".csv" # CSV file name

with open(filename, mode='x', newline='', encoding='utf-8') as csvfile:
    #creating csv writer object
    csvwriter = csv.writer(csvfile, dialect='excel')
    #print header row
    csvwriter.writerow(["Date/Time", "Pressure", "Flowrate", "Displacement"])

while True:
    # 'g' "go" start scan
    if keyboard.is_pressed('g' or 'G'):
        keyboard.read_key()
        acquiring = True
        send_cmd("start")
          
    # 's' stop scan
    if keyboard.is_pressed('s' or 'S'):
        keyboard.read_key()
        send_cmd("stop")
        time.sleep(1)
        ser.flushInput()
        print("")
        print("stopped")
        acquiring = False
        
    # 'r' reset counter
    if keyboard.is_pressed('r' or 'R'):
        keyboard.read_key()
        send_cmd("reset 1")
        
    # 'q' exit
    if keyboard.is_pressed('q' or 'Q'):
        keyboard.read_key()
        send_cmd("stop")
        ser.flushInput()
        break

    while (ser.inWaiting() > (2 * len(slist))):
        t = datetime.datetime.now()
        s = t.strftime('%Y-%m-%d %H:%M:%S.%f')
        head = s[:-7]               # everything up to the '.'
        tail = s[-7:]               # the '.' and the 6 digits after it
        f = float(tail)
        temp = "{:.03f}".format(f)  # for Python 2.x: temp = "%.3f" % f
        new_tail = temp[1:]         # temp[0] is always '0'; get rid of it
        current_time = head + new_tail

        # Append time data to 0th index of list
        # dataList_curr.append(current_time)

        for i in range(len(slist)):
            # The four LSBs of slist determine measurement function
            function = ((slist[slist_pointer]) & (0xf))
            # Two bytes per sample
            bytes = ser.read(2)

            if (function < 8):
                # Analog input channel
                result = (range_table[slist_pointer] * int.from_bytes(bytes, byteorder='little', signed=True) / 32768)
                if (i == 0):
                    # Pressure (Pa)
                    result = (result * (2500 / 750) * 90 / 2)
                    
                elif (i == 1):
                    # Pressure (Pa)
                    pressure_pa = (result * (2500 / 750) * 90 / 2)
                    
                    # Pressure (w.c)
                    pressure_wc = pressure_pa / 250
                    
                    # Diameter of blower outlet (in)
                    outlet_dia = 8 
                    
                    # Area of blower inlet (ft^2)
                    duct_area = ((math.pi * (outlet_dia/12)) ** 2) 
                    
                    # Density of dry air (lbs/ft^3)
                    dryair_density = 0.075 
                    
                    # Pitot tube coefficient = 0.81
                    pitot_coef = 0.81
                    
                    # Air flowrate (m^3/s)
                    result = (duct_area * 1096.2 * pitot_coef * math.sqrt(abs((pressure_wc / dryair_density))) * 0.00047194745)
                    
                else:
                    if (cycle_count > 4):
                        # Laser Sensor measurements (mm)
                        result = result * 1000 
                    else:
                        result = 0

                if(cycle_count > 4):
                    if(int(slist_pointer) == 2): 
                        dataList_curr.append(float(round(result, 0))) # Append analog channel i+1 data
                    else:
                        dataList_curr.append(float(round(result, 3))) # Append analog channel i+1 data

            elif (function == 8):
                # Digital input channel
                result = ((int.from_bytes(bytes, byteorder='big', signed=False)) & (0x007f))
                dataList_curr.append(result)

            elif (function == 9):
                # Rate input channel
                result = ((int.from_bytes(bytes, byteorder='little', signed=True) + 32768) / 65535 * (range_table[slist_pointer]))
                dataList_curr.append(result)

            else:
                # Counter input channel
                result = ((int.from_bytes(bytes, byteorder='little', signed=True)) + 32768)
                dataList_curr.append(result)

            # Get the next position in slist
            slist_pointer += 1

            if (slist_pointer + 1) > (len(slist)):
                if (cycle_count > 4):
                    # End of a pass through slist items...output, reset, continue
                    if (cycle_count == 5):
                        dataList_ref = dataList_curr.copy() # copy the laser distance at the start of the test

                    # dataList_prev initialized to [0,0,0,0,0] for first pass
                    for j in range(len(dataList_curr)):
                        if (j == 0 or j == 1):
                            dataList_newcurr.append(float(round(dataList_curr[0], 3)))
                        else:
                            # calibration_factor = 0.153
                            diff = 0
                            diff = abs(float(dataList_curr[j]) - float(dataList_ref[j]))
                            dataList_newcurr.append(float(round(diff, 3)))

                    # Print to console (prints raw data rather than diff)
                    #print(current_time + " | " + label + " " + output_string.rstrip(", "))
                    print(current_time + " | " + "Chamber Pressure (Pa): " + str(dataList_newcurr[0]) + " | " + "Flow Rate (m^3/s): " + str(dataList_newcurr[1]) + " | " + "Displacemet of Valve (mm) " + str(dataList_newcurr[2]))

                    # Insert timestamp at beginning (index 0) of dataList_newcurr before writing to .csv
                    dataList_newcurr.insert(0, current_time)

                    # Write to csv file (writes the differences)
                    with open(filename, 'a+', newline='', encoding='utf-8') as csvfile:
                        # Creating csv writer object
                        csvwriter = csv.writer(csvfile, dialect='excel')
                        # Print row of csv data
                        csvwriter.writerow(dataList_newcurr)

                    # Copying current data into previous data for next passthrough
                    #dataList_prev = Cloning(dataList_curr)
                    
                    # Clearing the current data list for next row of csv printing
                    dataList_newcurr.clear()
                    dataList_curr.clear()

                slist_pointer = 0
                time.sleep(0.7) # Delay
                cycle_count += 1 # Increment the while loop cycle count

ser.close()
SystemExit
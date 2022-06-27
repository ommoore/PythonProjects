#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Oliver Moore
# Created Date: 07/12/2018
# version = '1.0'
# ---------------------------------------------------------------------------
""" Trinamic Motor Command Library (TMCL) with own API and testbench script 
designed by the Spartan Hyperloop 3 (2018) propulsion team for motor control. 
(4x) Synchronous single-axis in-hub BLDC motors are connected to (4x) 
TMCM-1630 driver/BB-1630 baseboard modules. TMCL commands are sent over USB 
from Raspberry Pi to (4x) TMCM modules, with RS232, RS485, and CAN as 
alternative options. Currently testing position-mode PI tracking with forward
and reverse operations.

Hardware:
    - (x4) (70mm x 80mm x 115mm) low-noise E-WHEELIN in-hub brushless DC motors
    - (x4) TMCM-1630 single-axis BLDC motor driver (10A/48VDC) 
    - (x4) BB-1630 baseboard shield for TMCM module with: 
             standalone operation or RS232, CAN, RS485, USB
    - (x4) USB-A to USB-B cables
    - (x1) Raspberry Pi 3 Model B+
    - (x8) Venom Flight Pack 5000 LiPo - 25C 5000mAH 14.8V packs 
             2S1P per TMCM/BB-1630 module. 29.6V 5Ah Secondary Battery Pack
"""
# ---------------------------------------------------------------------------
import sys
#Raspberry Pi Python version (from 2018)
sys.path.append("/home/pi/.local/lib/python2.7/site-packages")
#sys.path.append("./TMCL")
from serial import Serial
import math
import TMCL

## serial-address as set on the TMCM module.
MODULE_ADDRESS = 1

print("Connecting to USB serial ports..")
## Open the USB serial ports
serial_port0 = Serial("/dev/ttyACM0")
serial_port1 = Serial("/dev/ttyACM1")
serial_port2 = Serial("/dev/ttyACM2")
serial_port3 = Serial("/dev/ttyACM3")

print("Connecting to TMCL serial busses..")
## Create a Bus instance using the open serial port
bus0 = TMCL.connect(serial_port0)
bus1 = TMCL.connect(serial_port1)
bus2 = TMCL.connect(serial_port2)
bus3 = TMCL.connect(serial_port3)

print("Creating motor modules..")
## Create motor modules
motor0 = bus0.get_motor(MODULE_ADDRESS)
motor1 = bus1.get_motor(MODULE_ADDRESS)
motor2 = bus2.get_motor(MODULE_ADDRESS)
motor3 = bus3.get_motor(MODULE_ADDRESS)

print("Restarting Trinamic Module Timers..")
## Restart/Reinitialize the Trinamic Module Timers
motor0.send(5,31,0,0)
motor1.send(5,31,0,0)
motor2.send(5,31,0,0)
motor3.send(5,31,0,0)

## //////////// API Definitions ////////////
## Motor parameter initializations
def motorParam():
    ## TMCL-IDE Commands
	print("Initializing motor parameters..")
    
    ##set commutation mode (FOC Hall Sensor)
    motor0.send(5, 159, 0, 6)
    motor1.send(5, 159, 0, 6)
    motor2.send(5, 159, 0, 6)
    motor3.send(5, 159, 0, 6)

    ##set hall sensor invert (True)
    motor0.send(5, 254, 0, 1)
    motor1.send(5, 254, 0, 1)
    motor2.send(5, 254, 0, 1)
    motor3.send(5, 254, 0, 1)

    ##set motor poles (20)
    motor0.send(5, 253, 0, 20)
    motor1.send(5, 253, 0, 20)
    motor2.send(5, 253, 0, 20)
    motor3.send(5, 253, 0, 20)

    ##set start current [1mA] (peak)
    motor0.send(5, 177, 0, 1000)
    motor1.send(5, 177, 0, 1000)
    motor2.send(5, 177, 0, 1000)
    motor3.send(5, 177, 0, 1000)

    ##set max current [6250mA] (peak)
    motor0.send(5, 6, 0, 6250)
    motor1.send(5, 6, 0, 6250)
    motor2.send(5, 6, 0, 6250)
    motor3.send(5, 6, 0, 6250)

    ##set max velocity [1700rpm]
    motor0.send(5, 4, 0, 1700)
    motor1.send(5, 4, 0, 1700)
    motor2.send(5, 4, 0, 1700)
    motor3.send(5, 4, 0, 1700)

    ##set acceleration [500rpm/s]
    motor0.send(5, 11, 0, 500)
    motor1.send(5, 11, 0, 500)
    motor2.send(5, 11, 0, 500)
    motor3.send(5, 11, 0, 500)

    ##set torque P (600)
    motor0.send(5, 172, 0, 600)
    motor1.send(5, 172, 0, 600)
    motor2.send(5, 172, 0, 600)
    motor3.send(5, 172, 0, 600)

    ##set torque I (1000)
    motor0.send(5, 173, 0, 1000)
    motor1.send(5, 173, 0, 1000)
    motor2.send(5, 173, 0, 1000)
    motor3.send(5, 173, 0, 1000)

    ##set velocity P (20175)
    motor0.send(5, 234, 0, 20175)
    motor1.send(5, 234, 0, 20175)
    motor2.send(5, 234, 0, 20175)
    motor3.send(5, 234, 0, 20175)

    ##set velocity I (20175)
    motor0.send(5, 235, 0, 20175)
    motor1.send(5, 235, 0, 20175)
    motor2.send(5, 235, 0, 20175)
    motor3.send(5, 235, 0, 20175)

    ##set position P (20175)
    motor0.send(5, 230, 0, 300)
    motor1.send(5, 230, 0, 300)
    motor2.send(5, 230, 0, 300)
    motor3.send(5, 230, 0, 300)

    ##set thermal winding time constant [ms]    
    motor0.send(5, 25, 0, 300)
    motor1.send(5, 25, 0, 300)
    motor2.send(5, 25, 0, 300)
    motor3.send(5, 25, 0, 300)

    ##set IIT counter limit
    motor0.send(5, 26, 0, 300)
    motor1.send(5, 26, 0, 300)
    motor2.send(5, 26, 0, 300)
    motor3.send(5, 26, 0, 300)
    

def fwd():
    ##SAP 0x1, 0x0, 0        set actual position
    print("Actual Position Set to 0.")
    motor0.send(5, 1, 0, 0)
    motor1.send(5, 1, 0, 0)
    motor2.send(5, 1, 0, 0)
    motor3.send(5, 1, 0, 0)

    ##SAP 140x6, 0x0, 1      enable velocity ramp
    print("Enabling Position Mode...")
    motor0.send(5, 146, 0, 1)
    print("Motor 0 Velocity Ramp: %s" % (motor0.send(6,146,0,0)))
    motor1.send(5, 146, 0, 1)
    print("Motor 1 Velocity Ramp: %s" % (motor1.send(6,146,0,0)))
    motor2.send(5, 146, 0, 1)
    print("Motor 2 Velocity Ramp: %s" % (motor2.send(6,146,0,0)))
    motor3.send(5, 146, 0, 1)
    print("Motor 3 Velocity Ramp: %s" % (motor3.send(6,146,0,0)))

    ##SAP 0x0, 0x0, 0x4E20    set target position
    print("Target Position set to 75ft.")
    motor0.send(5, 0, 0, 5730)
    print("Motor 0 Target Position: %s" % (motor0.send(6,0,0,0)))
    motor1.send(5, 0, 0, 5730)
    print("Motor 0 Target Position: %s" % (motor1.send(6,0,0,0)))
    motor2.send(5, 0, 0, 5730)
    print("Motor 2 Target Position: %s" % (motor2.send(6,0,0,0)))
    motor3.send(5, 0, 0, 5730)
    print("Motor 3 Target Position: %s" % (motor3.send(6,0,0,0)))

     ##WAIT FOR EVENT CODE NEEDED
    
def rev():
    ##SAP 0x0, 0x0, 0        set target position
    print("Target Position set to 0.")
    motor0.send(5, 0, 0, 0)
    motor1.send(5, 0, 0, 0)
    motor2.send(5, 0, 0, 0)
    motor3.send(5, 0, 0, 0)

    ##WAIT FOR EVENT CODE NEEDED

    ##SAP 140x6, 0x0, 0      disable velocity ramp
    print("Disabling velocity ramp...")
    motor0.send(5, 146, 0, 0)
    print("Motor 0 Velocity Ramp: %s" % (motor0.send(6,146,0,0)))
    motor1.send(5, 146, 0, 0)
    print("Motor 1 Velocity Ramp: %s" % (motor0.send(6,146,0,0)))
    motor2.send(5, 146, 0, 0)
    print("Motor 2 Velocity Ramp: %s" % (motor0.send(6,146,0,0)))
    motor3.send(5, 146, 0, 0)
    print("Motor 3 Velocity Ramp: %s" % (motor0.send(6,146,0,0)))

    ##MST 0              	stop motor
    print("Motors stopped.")
    motor0.send(3, 0, 0, 0)
    motor1.send(3, 0, 0, 0)
    motor2.send(3, 0, 0, 0)
    motor3.send(3, 0, 0, 0)

def readMotor0RPM():
    print("Motor 0 RPM: %s" % (motor0.send(6,3,0,0)))
    return motor0.send(6,3,0,0)
def readMotor1RPM():
    print("Motor 1 RPM: %s" % (motor1.send(6,3,0,0)))
    return motor1.send(6,3,0,0)
def readMotor2RPM():
    print("Motor 2 RPM: %s" % (motor2.send(6,3,0,0)))
    return motor2.send(6,3,0,0)
def readMotor3RPM():
    print("Motor 3 RPM: %s" % (motor3.send(6,3,0,0)))
    return motor3.send(6,3,0,0)
    
def readMotor0Pos():
    print("Motor 0 Pos(ft): %s" % (motor0.send(6,1,0,0)))
    return motor0.send(6,1,0,0)
def readMotor1Pos():
    print("Motor 1 Pos(ft): %s" % (motor1.send(6,1,0,0)))
    return motor1.send(6,1,0,0)
def readMotor2Pos():
    print("Motor 2 Pos(ft): %s" % (motor2.send(6,1,0,0)))
    return motor2.send(6,1,0,0)
def readMotor3Pos():
    print("Motor 3 Pos(ft): %s" % (motor3.send(6,1,0,0)))
    return motor3.send(6,1,0,0)
    
def readMotor0Current():
    print("Motor 0 Current(mA): %s" % (motor0.send(6,150,0,0)))
    return motor0.send(6,150,0,0)
def readMotor1Current():
    print("Motor 1 Current(mA): %s" % (motor1.send(6,150,0,0)))
    return motor1.send(6,150,0,0)
def readMotor2Current():
    print("Motor 2 Current(mA): %s" % (motor2.send(6,150,0,0)))
    return motor2.send(6,150,0,0)
def readMotor3Current():
    print("Motor 3 Current(mA): %s" % (motor3.send(6,150,0,0)))
    return motor3.send(6,150,0,0)

def readBoard0Temp():
    ADC0 = motor0.send(6,152,0,0)
    B = 3434
    RNTC0 = (9011.2/ADC0) - 2.2
    board0Temp = ((B * 298.16)/(B + (math.log(RNTC0/10)*298.16)))- 273.16
    print("Trinamic 0 Temperature(C): %s" % (board0Temp))
    return board0Temp
def readBoard1Temp():
    ADC1 = motor1.send(6,152,0,0)
    B = 3434
    RNTC1 = (9011.2/ADC1) - 2.2
    board1Temp = ((B * 298.16)/(B + (math.log(RNTC1/10)*298.16)))- 273.16
    print("Trinamic 1 Temperature(C): %s" % (board1Temp))
    return board1Temp
def readBoard2Temp():
    ADC2 = motor2.send(6,152,0,0)
    B = 3434
    RNTC2 = (9011.2/ADC2) - 2.2
    board2Temp = ((B * 298.16)/(B + (math.log(RNTC2/10)*298.16)))- 273.16
    print("Trinamic 2 Temperature(C): %s" % (board2Temp))
    return board2Temp
def readBoard3Temp():
    ADC3 = motor3.send(6,152,0,0)
    B = 3434
    RNTC3 = (9011.2/ADC3) - 2.2
    board3Temp = ((B * 298.16)/(B + (math.log(RNTC3/10)*298.16)))- 273.16
    print("Trinamic 3 Temperature(C): %s" % (board3Temp))
    return board3Temp
    
def readBoard0Voltage():
    print("Trinamic 0 Supply Voltage(V): %s" % (motor0.send(6,151,0,0)))
    return motor0.send(6,151,0,0)
def readBoard1Voltage():
    print("Trinamic 1 Supply Voltage(V): %s" % (motor1.send(6,151,0,0)))
    return motor1.send(6,151,0,0)
def readBoard2Voltage():
    print("Trinamic 2 Supply Voltage(V): %s" % (motor2.send(6,151,0,0)))
    return motor2.send(6,151,0,0)
def readBoard3Voltage():
    print("Trinamic 3 Supply Voltage(V): %s" % (motor3.send(6,151,0,0)))
    return motor3.send(6,151,0,0)

def readModule0RunTime(): 
    print("Trinamic 0 Runtime(min): %s" % (motor0.send(6,30,0,0)))
    return motor0.send(6,30,0,0)
def readModule1RunTime():
    print("Trinamic 1 Runtime(min): %s" % (motor1.send(6,30,0,0)))
    return motor1.send(6,30,0,0)
def readModule2RunTime(): 
    print("Trinamic 2 Runtime(min): %s" % (motor2.send(6,30,0,0)))
    return motor2.send(6,30,0,0)
def readModule3RunTime(): 
    print("Trinamic 3 Runtime(min): %s" % (motor3.send(6,30,0,0)))
    return motor3.send(6,30,0,0)

def readErrorFlags0():
    print("Trinamic 0 Error Flags: %s" % (motor0.send(6,156,0,0)))
    return motor0.send(6,156,0,0)
def readErrorFlags1():
    print("Trinamic 1 Error Flags: %s" % (motor1.send(6,156,0,0)))
    return motor1.send(6,156,0,0)
def readErrorFlags2():
    print("Trinamic 2 Error Flags: %s" % (motor2.send(6,156,0,0)))
    return motor2.send(6,156,0,0)
def readErrorFlags3():
    print("Trinamic 3 Error Flags: %s" % (motor3.send(6,156,0,0)))
    return motor3.send(6,156,0,0)

def clearIIT0():
    print("Clearing IIT flags of Module 0..")
    motor0.send(6,29,0,0)
def clearIIT1():
    print("Clearing IIT flags of Module 1..")
    motor1.send(6,29,0,0)
def clearIIT2():
    print("Clearing IIT flags of Module 2..")
    motor2.send(6,29,0,0)
def clearIIT3():
    print("Clearing IIT flags of Module 3..")
    motor3.send(6,29,0,0)

def readIIT0():
    print("Motor 0 Thermal Winding Constant: %s" % (motor0.send(6,25,0,0)))
    print("Motor 0 IIT Limit: %s" % (motor0.send(6,26,0,0)))
    print("Motor 0 IIT Sum: %s" % (motor0.send(6,27,0,0)))
    print("Motor 0 IIT Exceed Counter: %s" % (motor0.send(6,28,0,0)))
    return motor0.send(6,27,0,0)
def readIIT1():
    print("Motor 1 Thermal Winding Constant: %s" % (motor1.send(6,25,0,0)))
    print("Motor 1 IIT Limit: %s" % (motor1.send(6,26,0,0)))
    print("Motor 1 IIT Sum: %s" % (motor1.send(6,27,0,0)))
    print("Motor 1 IIT Exceed Counter: %s" % (motor1.send(6,28,0,0)))
    return motor1.send(6,27,0,0)
def readIIT2():
    print("Motor 2 Thermal Winding Constant: %s" % (motor2.send(6,25,0,0)))
    print("Motor 2 IIT Limit: %s" % (motor2.send(6,26,0,0)))
    print("Motor 2 IIT Sum: %s" % (motor2.send(6,27,0,0)))
    print("Motor 2 IIT Exceed Counter: %s" % (motor2.send(6,28,0,0)))
    return motor2.send(6,27,0,0)
def readIIT3():
    print("Motor 3 Thermal Winding Constant: %s" % (motor3.send(6,25,0,0)))
    print("Motor 3 IIT Limit: %s" % (motor3.send(6,26,0,0)))
    print("Motor 3 IIT Sum: %s" % (motor3.send(6,27,0,0)))
    print("Motor 3 IIT Exceed Counter: %s" % (motor3.send(6,28,0,0)))
    return motor3.send(6,27,0,0)

## //////////// Application ////////////
motorParam()
while(1):
    fwd()
    rev()

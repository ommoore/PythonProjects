# SHL_TrinamicHubMotor
  **Description:** \
Trinamic Motor Command Library (TMCL) paired with a user library and test application designed by the Spartan Hyperloop 3 (2018) propulsion team to achieve pod motor 
control for the SpaceX Hyperloop Competition. (4x) Synchronous single-axis wheel-hub brushless DC (BLDC) motors are connected to (4x) TMCM-1630 driver/BB-1630 baseboard 
modules. TMCL commands are sent over USB from Raspberry Pi to (4x) TMCM modules, with RS232, RS485, and CAN as alternative options. Currently testing position-mode PI 
tracking with four-quadrant motor operations (forward/reverse + acceleration/braking).

  **Hardware:**
  - (x4) (70mm x 80mm x 115mm) low-noise E-WHEELIN in-hub brushless DC motors
  - (x4) TMCM-1630 single-axis BLDC motor driver (10A/48VDC) 
  - (x4) BB-1630 baseboard shield for TMCM module with: 
         standalone operation or RS232, CAN, RS485, USB
  - (x4) USB-A to USB-B cables
  - (x1) Raspberry Pi 3 Model B+
  - (x8) Venom Flight Pack 5000 LiPo - 25C 5000mAH 14.8V packs 
         2S1P per TMCM/BB-1630 module. 29.6V 5Ah Secondary Battery Pack

  **Directory Contents:**
```
**SHL_TrinamicHubMotor**
│ -  README.md
│ -  position_mode_script.tmc  //Direct command script for Trinamic Software TMCL direct mode
| -  RPi_TMCM.py               //User Application  
| 
└───TMCL                       //TMCL - Trinamic Motor Control Library : NativeDesign, Alan Pich
    | - __init__.py
    │ - bus.py
    │ - commands.py
    | - motor.py
    | - reply.py
```

# PythonProjects

## PiCamera_RemoteRec
  **Description:** \
  A Raspberry Pi project to remotely record an event using a PiCamera circular stream and PyAudio microphone capture stream. Video (.h264) and
  audio (.wav) captures are muxed using FFmpeg (.mkv) and saved to the Pi's integrated SD card. The AV stream recordings are remotely triggered
  by an interrupt signal originating from an Arduino GPIO connected to GPIO pin 5 on the Pi. Interrupt could be generated from a sensor reading,
  timer, or other event.
  
  **Hardware:**
  - Raspberry Pi 3 B+
  - Raspberry Pi Camera Module 2
  - Adafruit Mini USB microphone
  - Arduino Mega2560

## PyVisa_SpectrumAnalyzer
  **Description:** \
  Using PyVisa (Python wrapper for VISA - Virtual Instrument Software Architecture) to interface with Spectrum Analyzer over USB. A csv writer object 
  is used to write the formatted time-stamped frequency (Hz) and amplitude (dB) data into .csv file. File is created with max permissions (RWX all users) 
  and filename checked for uniqueness, otherwise user will be prompted to enter new filename.

## SHL_TrinamicHubMotor
  **Description:** \
  Trinamic Motor Command Library (TMCL) with own API and testbench script designed by the Spartan Hyperloop 3 (2018) propulsion team for motor control.
  (4x) Synchronous single-axis in-hub BLDC motors are connected to (4x) TMCM-1630 driver/BB-1630 baseboard modules. TMCL commands are sent over USB
  from Raspberry Pi to (4x) TMCM modules, with RS232, RS485, and CAN as alternative options. Currently testing position-mode PI tracking with forward
  and reverse operations.

  **Hardware:**
  - (x4) (70mm x 80mm x 115mm) low-noise E-WHEELIN in-hub brushless DC motors
  - (x4) TMCM-1630 single-axis BLDC motor driver (10A/48VDC) 
  - (x4) BB-1630 baseboard shield for TMCM module with: 
         standalone operation or RS232, CAN, RS485, USB
  - (x4) USB-A to USB-B cables
  - (x1) Raspberry Pi 3 Model B+
  - (x8) Venom Flight Pack 5000 LiPo - 25C 5000mAH 14.8V packs 
         2S1P per TMCM/BB-1630 module. 29.6V 5Ah Secondary Battery Pack

# PythonProjects

## DATAQ_CSV
  **Description:** \
  Python app to read DAQ analog sensor data and store as csv file.
  Using DATAQ Instruments DI-4718B DAQ with DI-8B41-02 +/-5V amplifier 
  modules to read analog sensor data from SM9236 differential pressure 
  sensor, FS4000 mass flow sensor, and E18-D80NK IR proximity sensor. Test 
  app expects user keypress to start, stop, reset, and exit. Timestamped 
  analog sensor data is stored in .csv format and user-prompted filename 
  will be checked for uniqueness, to avoid overwriting existing saved data.
  WinDAQ software can be used to view and verify the data directly from DAQ.
  
  **Hardware:**
  - DATAQ Instruments DI-4718B 8-channel Ethernet Data Logger and Data 
    Acquisition System for DI-8B Amplifiers.
  - (x3) DI-8B41-02 Isolated ±5V 1kHz bandwidth 8B-style Amplifier modules
  - SM9236 Differential Pressure Sensor (Analog 0-5V)
  - FS4000 Mass Flow Sensor (Analog 0-5V)
  - E18-D80NK Infrared Proximity Sensor (Analog 0-5V)
    
  **Software:**
  - WinDAQ Recording and Playback Software (free) (optional)
	
## PiCamera_RemoteRec
  **Description:** \
  A Raspberry Pi project to remotely record an event using a PiCamera circular stream and PyAudio microphone capture stream. Video (.h264) and
  audio (.wav) captures are muxed using FFmpeg (.mkv) and saved to the Pi's integrated SD card. The AV stream recordings are triggered
  by an interrupt signal originating from an Arduino GPIO connected to pin 5 on the Pi. The interrupt could be generated from a sensor reading,
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
  Trinamic Motor Command Library (TMCL) paired with a user library and test application designed by the Spartan Hyperloop 3 (2018) propulsion team to achieve 
  pod motor control for the SpaceX Hyperloop Competition. (4x) Synchronous single-axis wheel-hub brushless DC (BLDC) motors are connected to 
  (4x) TMCM-1630 driver/BB-1630 baseboard modules. TMCL commands are sent over USB from Raspberry Pi to (4x) TMCM modules, with RS232, RS485, and CAN as 
  alternative options. Currently testing position-mode PI tracking with four-quadrant motor operations (forward/reverse + acceleration/braking).

  **Hardware:**
  - (x4) (70mm x 80mm x 115mm) low-noise E-WHEELIN wheel-hub BLDC motors
  - (x4) TMCM-1630 single-axis BLDC motor driver (10A/48VDC) 
  - (x4) BB-1630 baseboard shield for TMCM module with: 
         standalone operation or RS232, CAN, RS485, USB
  - (x4) USB-A to USB-B cables
  - (x1) Raspberry Pi 3 Model B+
  - (x8) Venom Flight Pack 5000 LiPo - 25C 5000mAH 14.8V packs 
         2S1P per TMCM/BB-1630 module. 29.6V 5Ah Secondary Battery Pack

  **Software:**
  - TMCM-BLDC-FOC
  - TMCL-IDE 3.0

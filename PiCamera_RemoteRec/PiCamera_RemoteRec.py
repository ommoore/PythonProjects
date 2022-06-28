#!/usr/bin/python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By : Oliver Moore
# version = '1.0'
# ---------------------------------------------------------------------------
""" A Raspberry Pi project to remotely record an event using a PiCamera 
circular stream and PyAudio microphone capture stream. Video (.h264) and audio 
(.wav) captures are muxed using FFmpeg (.mkv) and saved to the Pi's integrated 
SD card. The AV stream recordings are remotely triggered by an interrupt signal 
originating from an Arduino GPIO connected to GPIO pin 5 on the Pi. Interrupt
could be generated from a sensor reading, timer, or other event.

Hardware:
    - Raspberry Pi 3 B+
    - Raspberry Pi Camera Module 2
    - Adafruit Mini USB microphone
    - Arduino Mega2560
"""
# ---------------------------------------------------------------------------
import RPi.GPIO as GPIO
import picamera, pyaudio, wave, subprocess

# Definitions
doneRecording = False
arduino_pin = 29   # GPIO5 == Pin29 (physical)
readyToRecord = False

# Callback when GPIO pin 5 is pulled low by Arduino.
def arduino_callback(channel):
    print('Falling Edge detected on channel %s from Arduino!' %channel)
    global readyToRecord
    readyToRecord = True
    print('PiCamera is ready to record!')

def stream_recording():
    global doneRecording
    doneRecording = False    
    
    # PyCamera Circular Stream
    camera.start_recording(videostream, format='h264')
    while ~doneRecording:
        camera.wait_recording(1)
        
        # If Arduino interrupt is detected
        if readyToRecord:
            frames = []
            
            # PyAudio Stream
            print("PyCamera and PyAudio recording.")
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = audiostream.read(CHUNK)
                frames.append(data)
            print("Done recording!")
            
            # Keep 300 seconds of recorded videostream
            videostream.copy_to('testvideo.h264')
            print('Saving recording to testvideo.h264.')
            
            audiostream.stop_stream()
            audiostream.close()
            audio.terminate()     
            print('Ending PiAudio stream.')
            
            camera.stop_recording()
            camera.close()
            print('Ending PiCamera stream.')
            
            # Create mic .wav file from audiostream data
            wf = wave.open('testaudio.wav', 'wb')                              
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            
            doneRecording = True
                
    # After recording.. combine .h264 and .wav files into .mkv format
    cmd = 'ffmpeg -i testaudio.wav -i testvideo.h264 -shortest -c:v copy -c:a aac recording1.mkv'
    subprocess.call(cmd, shell=True)                                    
    print('FFmpeg muxing complete.')
        
## GPIO Inits
# Support for Pi pin numbers, instead of BCM channel names from Broadcom SOC
GPIO.setmode(GPIO.BOARD) 
# Set GPIO Pin 5 as Input (from Arduino)
GPIO.setup(arduino_pin, GPIO.IN)
# Non-blocking implementation to detect interrupt and trigger callback
GPIO.add_event_detect(arduino_pin, GPIO.FALLING, callback=arduino_callback)

## PiCamera Inits
with picamera.PiCamera() as camera:
    camera.resolution = (1024, 768)
    camera.framerate = 30

    ## PyAudio Inits
    audio = pyaudio.PyAudio()
    CHUNK = 8192                # Number of bytes per piece of sound
    FORMAT = pyaudio.paInt16    # Audio format (16 bit integer)
    CHANNELS = 1                # Number of channels
    RATE = 44100                # Sample Rate
    RECORD_SECONDS = 300        # Recording length
    
    audiostream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
    
    # Stream Init
    # Start a circular stream of length 5 minutes at bitrate 17Mbps (default)
    with picamera.PiCameraCircularIO(camera, seconds=300) as videostream:
        stream_recording()
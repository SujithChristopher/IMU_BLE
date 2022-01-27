import cv2
import os
import pandas as pd
import numpy as np

# import the opencv library
import cv2
import threading
import msgpack as mp
import msgpack_numpy as mpn
from datetime import datetime
import pickle

class recorder():
    
    def __init__(self):
        self.a = None
        self.vid = cv2.VideoCapture(0)
        # fourcc = cv2.VideoWriter_fourcc(*'XVID')
        # ret, frame = self.vid.read()
        # h,w,_ = frame.shape
        # self.out = cv2.VideoWriter('output.avi', fourcc, 30.0, (w,h))
        
        self.video_file = open("output.pickle", "wb")
        
    def camera(self):
        # define a video capture object
               
        while(True):
            try:

                ret, frame = self.vid.read()
                if ret:
                    cv2.imshow('frame', frame)
                    tm = datetime.now()
                    # print(tm)
                    
                    # self.out.write(frame)
                    pickle.dump([tm, frame], self.video_file)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    
                    break
            except:
                pass
        
        # After the loop release the cap object
        self.vid.release()
        self.video_file.close()
        # self.out.release()
        # Destroy all the windows
        cv2.destroyAllWindows()
    
    def ble(self):
        pass
    
"""
A simple program to read IMU data at 100Hz from the Arduino Nano 33 IOT board.
"""

import asyncio
from multiprocessing import ProcessError
import struct
import sys
from typing import Dict
import keyboard

import bleak
from bleak import BleakClient
from bleak import discover
import csv




# These values have been randomly generated - they must match between the Central and Peripheral devices
# Any changes you make here must be suitably made in the Arduino program as well
IMU_UUID = '13012F01-F8C3-4F4A-A8F4-15CD926DA146'
IMU_UUID1 = '13012F05-F8C3-4F4A-A8F4-15CD926DA146'

# Class for handling BLE communication with a Nano board for receiving IMU data.
class NanoIMUBLEClient(object):
    
    def __init__(self, uuid:str) -> None:
        super().__init__()
        self._client = None
        self._device = None
        self._connected = False
        self._running = False
        self._uuid = uuid
        self._found = False
        self._data = {"ax": 0.0, "ay": 0.0, "az": 0.0,
                      "gx": 0.0, "gy": 0.0, "gz": 0.0} 
        self.newdata = False
        self.printdata = True
        
        self.counter = 0
        self._csv_file = open('outputdata.csv', 'w')
        self._csv = csv.writer(self._csv_file)
        self._csv.writerow(["time","ax", "ay", "az", "gx", "gy", "gz"])
        
    
    @property
    def connected(self) -> bool:
        return self._connected
    
    @property
    def data(self) -> Dict:
        return self._data

    @property
    def uuid(self) -> str:
        return self._uuid

    @property
    def running(self) -> bool:
        return self._running
    
    @property
    def device(self):
        return self._device
    
    async def connect(self) -> None:
        if self._connected:
            return
        
        # Currently not connected.
        print('Arduino Nano IMU Service')
        print('Looking for Peripheral Device...')
        devices = await discover()
        for d in devices:
            
            if 'BLE LEFT'in d.name:
                self._found = True
                self._device = d
                sys.stdout.write(f'Found Peripheral Device {self._device.address}. ')
                break
            
            if 'BLE RIGHT'in d.name:
                self._found = True
                self._device = d
                sys.stdout.write(f'Found Peripheral Device {self._device.address}. ')
                break
        
        # Connect and do stuff.
        async with BleakClient(d.address) as self._client:
            sys.stdout.write(f'Connected.\n')
            self._connected = True
            # Start getting data.
            await self.start()
            # Run while connected.
            while self._connected:
                if self._running:
                    # Print data.
                    if self.printdata and self.newdata:                        
                        self.print_newdata()
                        self.newdata = False
                    await asyncio.sleep(0)
    
    async def disconnect(self) -> None:
        if self._connected:
            # Stop notification first.
            self._client.stop_notify()
            self._client.disconnect()
            self._connected = False
            self._running = False
    
    async def start(self) -> None:
        if self._connected:
            # Start notification
            await self._client.start_notify(self._uuid, self.newdata_hndlr)
            self._running = True
    
    async def stop(self) -> None:
        if self._running:
            # Stop notification
            await self._client.stop_notify(self._uuid)
        
    def newdata_hndlr(self, sender, data):
        self._data['ax'] = struct.unpack('<f', bytes(data[0:4]))[-1]
        self._data['ay'] = struct.unpack('<f', bytes(data[4:8]))[-1]
        self._data['az'] = struct.unpack('<f', bytes(data[8:12]))[-1]
        self._data['gx'] = struct.unpack('<f', bytes(data[12:16]))[-1]
        self._data['gy'] = struct.unpack('<f', bytes(data[16:20]))[-1]
        self._data['gz'] = struct.unpack('<f', bytes(data[20:24]))[-1]
        self.newdata = True
    
    def print_newdata(self) -> None:
        _str = ("\r Accl: " +
                f"{self.data['ax']:+1.3f}, " + 
                f"{self.data['ay']:+1.3f}, " + 
                f"{self.data['az']:+1.3f} | " +
                "Gyro: " +
                f"{self.data['gx']:+3.3f}, " +
                f"{self.data['gy']:+3.3f}, " +
                f"{self.data['gz']:+3.3f}")
        nw = datetime.now()
        
        # self._csv.writerow([str(nw), self.data['ax'], self.data['ay'], self.data['az'] , self.data['gx'] , self.data['gy'] , self.data['gz'] ])
        
        sys.stdout.write(_str)
        sys.stdout.flush()
        
        


async def run_imu():
    # Create a new IMU client.
            
    imu_client_1 = NanoIMUBLEClient(IMU_UUID)
    imu_client_2 = NanoIMUBLEClient(IMU_UUID1)
    await imu_client_1.connect()
    await imu_client_2.connect()

#intermediate callback to execure async funciton    
def between_callback():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(run_imu())
    loop.close()
    
# running camera application
def run_camera():
    rec = recorder()
    rec.camera()

if __name__ == "__main__":
    # First create an object
    loop = asyncio.get_event_loop()
        
    t1 = threading.Thread(target=between_callback)
    t2 = threading.Thread(target=run_camera)
  
    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()
  
    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()
    
    
    
    

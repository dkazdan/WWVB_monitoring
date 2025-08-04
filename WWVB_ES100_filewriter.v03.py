"""
2 August 2025
DK

Monitor Teensy serial port looking for ES100 decodes of WWVB.
Did not have any data morning of 3 August.

Try the other WWVB receiver, which seems to be receiving a time
code about every three minutes all day.

Try a piece of Teensy test code that just writes a line per second
to the port.

v02 Better checking of incoming serial data with bufferBytes = ser.inWaiting()
"""

import serial
import os

# Open the serial port
ser0 = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser1 = serial.Serial('/dev/ttyACM1', 9600, timeout=1)

# function to read specified serial port
def readPort(port=0):
    if   port == 0:
        if ser0.inWaiting():
            line = ser0.readline().decode('utf-8').strip() # remove leading and trailing whitespace
        else:
            return
    elif port == 1:
        if ser0.inWaiting():
            line = ser1.readline().decode('utf-8').strip()
        else:
            return
    else:
        print('error in port number')

        # Check for expected format
        if line.startswith("date: "):
            date_time_str = line[6:].strip()  # Remove "date: " prefix
            date_str = date_time_str[0:8]         # date part only YY:MM:DD
            time_str = date_time_str[16:25]       # time part only HH:MM:SS
            month_str= date_str[0:5]              # YY:MM part only (WWVB time gives 2-digit year)
            try:
                # Open a filename numbered by serial port number        
                filename = f"/home/WWVB/WWVB_decodes/{month_str}_WWVB{str(port)}.txt"

                # Append the line to the file
                with open(filename, "a") as f:
                    f.write(line + "\n")

                print(f"Line appended to {filename} at {time_str}")
                #line = '' # reset and wait for next data line
            except Exception as e:
                print(f"Error processing date line: {e}")
        return


# Read one line from serial
#line = ''
while (True):
    readPort(port=0)
    readPort(port=1)

# Close serial port
ser0.close()
ser1.close()


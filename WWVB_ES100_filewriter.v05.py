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
v03 TODO: Get second receiver working, writing to different file.
    Seemed to break that code, perhaps by adding the second serial port or by
    factoring out the code as a function.  Try again.
v04
    First, just rename the serial port and its writing file to suffix 0 and verify that that works.
v05
    Start saving the data from the two receivers in separate files
"""

import serial
import os

# Open the serial port
ser0 = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
# added second serial port to see if that disturbs anything, haven't implemented it yet.
# 0227 UTC, have three decodes. TODO: Try recording from ACM1, also.
# 1200 UTC, there are overnight decodes on ser0, so opening ser1 didn't affect that.
#  Now try reading from that port, just checking for data.
ser1 = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
# the second receiver is ACM1

# Read one line from serial
#line = ''
while (True):
    if ser0.inWaiting():
        line = ser0.readline().decode('utf-8').strip() # remove leading and trailing whitespace

        # Check for expected format
        if line.startswith("date: "):
            date_time_str = line[6:].strip()  # Remove "date: " prefix
            date_str = date_time_str[0:8]         # date part only YY:MM:DD
            time_str = date_time_str[16:25]       # time part only HH:MM:SS
            month_str= date_str[0:5]              # YY:MM part only (WWVB time gives 2-digit year)
            try:
                # year_month = "-".join(date_str.split("-")[:2])  # Get YYYY-MM
        
                filename = f"/home/WWVB/WWVB_decodes/{month_str}_WWVB0.txt"

                # Append the line to the file
                with open(filename, "a") as f:
                    f.write(line + "\n")

                print(f"Line appended to {filename} at {time_str}")
                #line = '' # reset and wait for next data line
            except Exception as e:
                print(f"Error processing date line: {e}")
                
    if (ser1.inWaiting() > 0): # Second radio, on serial port 1
        line = ser1.readline().decode('utf-8').strip() # remove leading and trailing whitespace

        # Check for expected format
        if line.startswith("date: "):
            date_time_str = line[6:].strip()  # Remove "date: " prefix
            date_str = date_time_str[0:8]         # date part only YY:MM:DD
            time_str = date_time_str[16:25]       # time part only HH:MM:SS
            month_str= date_str[0:5]              # YY:MM part only (WWVB time gives 2-digit year)
            try:
                # year_month = "-".join(date_str.split("-")[:2])  # Get YYYY-MM
        
                filename = f"/home/WWVB/WWVB_decodes/{month_str}_WWVB1.txt"

                # Append the line to the file
                with open(filename, "a") as f:
                    f.write(line + "\n")

                print(f"Line appended to {filename} at {time_str} Z")
                #line = '' # reset and wait for next data line
            except Exception as e:
                print(f"Error processing date line: {e}")

# Close serial port
ser0.close()
ser1.close()


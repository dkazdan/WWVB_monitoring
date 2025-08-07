"""
WWVB_graphing.py
Reads in files as formatted by the data collection programs
from the ES100 WWVB phase signal receiver.
Plots indicate correct decode times.
Started 7 August 2025
DK
"""


from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# prompt: make a function from the above code. Use the string as the argument, return the datetime object

def parse_datetime_string(date_string):
  """
  Parses a specific date and time string format into a datetime object.

  Args:
    date_string: A string in the format "date: YY:MM:DD  time: HH:MM:SS".

  Returns:
    A datetime object representing the parsed date and time.
  """
  # Extract date and time parts
  date_part = date_string.split("date: ")[1].split("  ")[0]
  time_part = date_string.split("time: ")[1]

  # Reformat the date and time parts into a single string parsable by datetime
  datetime_string = f"{date_part} {time_part}"

  # Define the format of the datetime string
  datetime_format = "%y:%m:%d %H:%M:%S"

  # Create the datetime object
  datetime_object = datetime.strptime(datetime_string, datetime_format)

  return datetime_object


# prompt: Generate datetime objects from the file "C:\Users\dxk10\Downloads\2025_07_WWVB_log"

# The path provided "C:\Users\dxk10\Downloads\2025_07_WWVB_log" is a local Windows path.
# To read a file in Google Colab, you need to either:
# 1. Upload the file to your Colab session's temporary storage.
# 2. Mount your Google Drive and access the file there.
# 3. Access the file from Google Cloud Storage or other cloud storage.

# Assuming the file has been uploaded to the current Colab session's working directory
# or placed in a location accessible by providing a relative or absolute path within Colab.

file_path = '/home/WWVB/WWVB_decodes/25:08_WWVB1.txt' # Replace with the actual path to the file in Colab
#file_path = '2025_07_WWVB_OBJ_log' # Replace with the actual path to the file in Colab

datetime_objects_list = []

try:
    with open(file_path, 'r') as f:
        for line in f:
            # Assuming each relevant line in the file starts with "date:"
            if line.strip().startswith('date:'):
                try:
                    # Use the existing parse_datetime_string function
                    datetime_obj = parse_datetime_string(line.strip())
                    datetime_objects_list.append(datetime_obj)
                except Exception as e:
                    print(f"Could not parse line: {line.strip()} - {e}")

except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
except Exception as e:
    print(f"An error occurred while reading the file: {e}")

# Now datetime_objects_list contains datetime objects parsed from the file
print(f"Successfully parsed {len(datetime_objects_list)} datetime objects.")

# Example of how to use the list
# for dt_obj in datetime_objects_list:
#     print(dt_obj)

# You can now use the `datetime_objects_list` for further processing,
# like plotting multiple points on the timeline.


# prompt: repeat above but make subplot titles smaller

from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Organize datetime objects by date
daily_data = defaultdict(list)
for dt_obj in datetime_objects_list:
    daily_data[dt_obj.date()].append(dt_obj)

if not daily_data:
    print("No data to plot.")
else:
    # Get the unique dates and sort them
    dates_to_plot = sorted(daily_data.keys())
    num_days = len(dates_to_plot)

    # Create a figure and axes, one for each day
    # Increased the height multiplier in figsize for more vertical space
    fig, axes = plt.subplots(num_days, 1, figsize=(15, num_days * 0.8), squeeze=False)

    # Add vertical spacing between subplots
    plt.subplots_adjust(hspace=0.8) # Adjust hspace value to control vertical spacing

    # Iterate through each day and its data
    for i, date_to_plot in enumerate(dates_to_plot):
        ax = axes[i, 0] # Get the axis for the current day

        # Get the datetime objects for this specific day
        datetimes_for_day = daily_data[date_to_plot]

        # Define the start and end of the UTC day for the current date
        start_of_day = datetime.combine(date_to_plot, datetime.min.time())
        end_of_day = start_of_day + timedelta(days=1)

        # Draw the horizontal line representing the UTC day
        ax.hlines(0, start_of_day, end_of_day, color='blue', lw=2)

        # Draw red dots for each datetime object on this day
        for dt in datetimes_for_day:
            ax.plot(dt, 0, 'ro') # 'ro' means red circle marker

        # Set the x-axis to display time
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        ax.xaxis.set_major_locator(mdates.HourLocator())
        ax.set_xlim([start_of_day, end_of_day]) # Ensure the x-axis covers the full day

        # Remove y-axis
        ax.yaxis.set_visible(False)
        ax.set_yticks([]) # Explicitly remove y-axis ticks

        # Set title for each subplot with a smaller font size
        ax.set_title(f'{date_to_plot.strftime("%Y-%m-%d")}', fontsize=10) # Smaller title

        # Remove x-axis labels for all but the last plot
        if i < num_days - 1:
            ax.set_xlabel('')
            ax.tick_params(labelbottom=False)
        else:
            ax.set_xlabel('Time (UTC)') # Add x-axis label only to the last plot

    # Add a main title to the figure
    fig.suptitle('WWVB Phase-Shift Signal Received Times by Day\nCleveland, Ohio', y=1.15) # Adjust y for positioning

    # Improve layout
    fig.autofmt_xdate()
    # We use subplots_adjust for spacing instead of tight_layout in this case.
    # plt.tight_layout()

    # Show the plot
    plt.savefig('JulyWWVB_high_sens.png')
    plt.show()


#!/usr/local/bin/python3

import codecs
import csv
import datetime
import getpass
import os
import pathlib
import platform

if platform.system() != "Windows":
    import pwd
else:
    import getpass
    import win32api    
    import win32net

from pathlib import Path

def dump(dict):
	for key, value in dict.items():
		print(key, "=", str(value))

def get_current_username():
	if platform.system() != "Windows":
		return pwd.getpwuid(os.getuid()).pw_name
	else:
		userName = win32api.GetUserName()
		info = win32net.NetUserGetInfo(None, userName, 4)
		dump(info)
		return getpass.getuser()
	
USER_NAME = get_current_username() 

# If your LibreView user name differs from the user name on your OS, set it here
# LIBRE_VIEW_USER = USER_NAME # 'FirstLast'
# Problem on Windows is getting First and Last name from the OS
# TODO find first and last name or get them as parameters or check for any matching patter file 
# in the input folder and use that (assumes only one user) 
LIBRE_VIEW_USER = 'ThierryPerraut'

# The iCloud (base) directory depends on the platform
APPLE_ICLOUD_DRIVE_BASE_PATH = '/Library/Mobile Documents'
WINDOWS_ICLOUD_DRIVE_BASE_PATH = os.sep + 'iCloudDrive'
IS_IOS = platform.machine().startswith("iPhone")
IS_WINDOWS = platform.uname().system == 'Windows'
IS_MAC = not(IS_IOS or IS_WINDOWS)

ICLOUD_DRIVE_DIR = ''

if IS_IOS:
	ICLOUD_DRIVE_DIR = '/private/var/mobile' + APPLE_ICLOUD_DRIVE_BASE_PATH
elif (IS_WINDOWS): #Windows for sure
	ICLOUD_DRIVE_DIR = str(Path.home()) + WINDOWS_ICLOUD_DRIVE_BASE_PATH
else: # Presumably a Mac
	ICLOUD_DRIVE_DIR = str(Path.home()) + APPLE_ICLOUD_DRIVE_BASE_PATH
	IS_MAC = True

if (IS_IOS):
	# I'm using the 'Pythonista 3' folder in my iCloud drive as base directory:
	ICLOUD_DIR = ICLOUD_DRIVE_DIR + '/iCloud~com~omz-software~Pythonista3/Documents'
else:
	ICLOUD_DIR = ICLOUD_DRIVE_DIR + os.sep + 'LibreView'


# Input file: assume the file was exported from LibreView today
INPUT_FILE_NAME = LIBRE_VIEW_USER + '_glucose_' + datetime.date.today().strftime("%#d-%#m-%Y") + '.csv'
INPUT_FILE_PATH = ''

# Input file: iCloud drive on iOS, Downloads folder on macOS
if IS_IOS:
	INPUT_DIR = ICLOUD_DIR
else: 
	INPUT_DIR = str(Path.home()) + os.sep + 'Downloads'	

# Output file: always iCloud. The condition is here for cloud deniers ;)
OUTPUT_FILE_NAME = datetime.date.today().isoformat() + "_blood_glucose.csv"

INPUT_FILE_PATH = INPUT_DIR + os.sep + INPUT_FILE_NAME
OUTPUT_FILE_PATH = ICLOUD_DIR + os.sep  + OUTPUT_FILE_NAME

codecs.register_error("strict", codecs.ignore_errors)
# with codecs.open(INPUT_FILE_PATH, 'rU', 'utf-8') as f_in, open(OUTPUT_FILE_PATH, 'w') as f_out:

if not os.path.exists(INPUT_FILE_PATH): 
	print("The input File " + INPUT_FILE_NAME + " does not exist")

if not os.path.isdir(ICLOUD_DIR): 
	print("The output Folder " + ICLOUD_DIR + " does not exist. Creating it.")
	path = pathlib.Path(ICLOUD_DIR)
	path.mkdir(parents=True, exist_ok=True)	


with codecs.open(INPUT_FILE_PATH, 'r', 'utf-8') as f_in, open(OUTPUT_FILE_PATH, 'w') as f_out:
	input_reader = csv.reader(f_in, delimiter=',')
	writer = csv.writer(f_out, delimiter=',')
	next(input_reader)
	next(input_reader)
	# Input data is expected in mmol/L units, and exported as is
	# If you'd rather use mg/dL, change the column name in the next line to 'Blood Glucose (mg/dL)'
	# If you'd rather use mmol, change the column name in the next line to 'Blood Glucose (mmol<180.1558800000541>/L)'
	# writer.writerow(['Start', 'Blood Glucose (mmol<180.1558800000541>/L)'])
	writer.writerow(['Start', 'Blood Glucose (mg/dL)'])
	for row in input_reader:
		timestamp = row[2]
		# For default date and 12h format, use this
		# iso_timestamp = datetime.datetime.strptime(timestamp, '%m-%d-%Y %I:%M %p').isoformat()
		iso_timestamp = datetime.datetime.strptime(timestamp, '%d-%m-%Y %H:%M').isoformat()
		measurement = row[4] if row[4] else row[5]
		if measurement:
			writer.writerow([iso_timestamp, measurement])

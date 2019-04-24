import csv
import codecs
import datetime

# Your LibreView user name
LV_USER = 'FirstLast'

# I'm using the 'Pythonista 3' folder in the iCloud drive as base directory
BASE_DIR = '/private/var/mobile/Library/Mobile Documents/iCloud~com~omz-software~Pythonista3/Documents/'

# Input and output files are expected to be in IN and OUT directories within the BASE_DIR
INPUT_FILE_NAME = BASE_DIR + '/IN/LV_' + LV_USER + '_Export_' + datetime.date.today().strftime("%m-%d-%Y") + '.csv'
OUTPUT_FILE_NAME = BASE_DIR + '/OUT/' + datetime.date.today().isoformat() + "_blood_glucose.csv"

codecs.register_error("strict", codecs.ignore_errors)
with codecs.open(INPUT_FILE_NAME, 'rU', 'utf-16-le') as f_in, open(OUTPUT_FILE_NAME, 'w') as f_out:
	input_reader = csv.reader(f_in, delimiter=',')
	writer = csv.writer(f_out, delimiter=',')
	next(input_reader)
	next(input_reader)
	# Input data is expected in mmol/L units, and exported as is
	writer.writerow(['Start', 'Blood Glucose (mmol<180.1558800000541>/L)'])
	for row in input_reader:
		timestamp = row[2]
		iso_timestamp = datetime.datetime.strptime(timestamp, '%m-%d-%Y %I:%M %p').isoformat()
		measurement = row[4] if row[4] else row[5]
		if measurement:
			writer.writerow([iso_timestamp, measurement])
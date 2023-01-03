####################################################################################################
#
#   THE PYTHON VERSION OF THIS SCRIPT IS STILL A WORK-IN-PROGRESS. DO NOT USE.
#
####################################################################################################

from pathlib import Path
import os.path
from os import path
import sys
from datetime import datetime,timedelta
import uuid
import random
import re

file_location = str(Path.home()) + "/calendar.ics"
break_length_options = [-90,-60,-30,0,0,0,15,15,15,30,30,60,90]
event_length_options = [15,15,30,30,30,30,30,45,45,60,60,60,60,60,60,60,60,90,90,90,120,120,120,240]

##### Start of script, stop editing here #####

if path.exists(file_location):
	print("\033[91m" + file_location + " already exists. Aborting..." + "\033[0m")
	sys.exit(1)

while True:
	user_input_year = input("Enter the year you'd like to create junk events for: ")
	if bool(re.search("^[12][0-9]{3}$", user_input_year)):
		break
	print("\033[91mPlease enter a valid year between 1000 to 2999\033[0m")

while True:
	user_input_month = input("Enter the month you'd like to create junk events for: ")
	if bool(re.search("(^[1-9]$)|(^1[0-2]$)", user_input_month)):	# Disallow leading zero in month as `datetime` does not allow it
		break
	print("\033[91mPlease enter a valid month between 1 to 12\033[0m")

regex_time = "^(([0-9])|([0-1][0-9])|([2][0-3]))([0-5][0-9])$"

while True:
	while True:
		user_input_begin_time = input("Enter your start time in 24-hour format without colons (ex: 0830): ")
		if bool(re.search(regex_time, user_input_begin_time)):
			break
		print("\033[91mPlease enter a valid 24-hour time without colons\033[0m")

	while True:
		user_input_end_time = input("Enter your end time in 24-hour format without colons (ex: 1700): ")
		if bool(re.search(regex_time, user_input_end_time)):
			break
		print("\033[91mPlease enter a valid 24-hour time without colons\033[0m")

	if user_input_begin_time < user_input_end_time:
		break
	print("\033[91mStart time is later than end time. Please try again\033[0m")

day_begin_hour = user_input_begin_time[0:2]
day_begin_minute = user_input_begin_time[2:4]
day_end_hour = user_input_end_time[0:2]
day_end_minute = user_input_end_time[2:4]

days_in_month = monthrange(user_input_year, user_input_month)[1]

calendar_template_begin = """BEGIN:VCALENDAR
PRODID:-//ZYLAI//iCal Fake Events Generator//EN
VERSION:2.0
METHOD:PUBLISH"""

ics_file = open(file_location, "a")
ics_file.write(calendar_template_begin)

for day in range(1, days_in_month + 1):
	date = datetime(user_input_year, user_input_month, day)

	if ((date.strftime('%A') == "Saturday") or (date.strftime('%A') == "Sunday")):
		continue

	day_begin = datetime(user_input_year, user_input_month, day, day_begin_hour, day_begin_minute)
	day_end = datetime(user_input_year, user_input_month, day, day_end_hour, day_end_minute)

	event_end = day_begin

	while (event_end < day_end):
		break_length = timedelta(minutes = random.choice(break_length_options))
		event_end = event_end + break_length
		event_begin = event_end
		event_length = timedelta(minutes = random.choice(event_length_options))
		event_end = event_begin + event_length

		event_template = """BEGIN:VEVENT
CLASS:PRIVATE
DESCRIPTION:\n
DTSTAMP:$((Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssZ"))
DTSTART:$($EventBegin.ToUniversalTime().ToString("yyyyMMddTHHmm00Z"))
DTEND:$($EventEnd.ToUniversalTime().ToString("yyyyMMddTHHmm00Z"))
PRIORITY:9
SEQUENCE:0
TRANSP:OPAQUE
UID:{}
END:VEVENT""".format(, , , str(uuid.uuid4()))

		ics_file.write(event_template)

calendar_template_end = "END:VCALENDAR"

ics_file.write(calendar_template_end)

ics_file.close

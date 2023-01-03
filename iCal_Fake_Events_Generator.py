####################################################################################################
#
#   THE PYTHON VERSION OF THIS SCRIPT IS STILL A WORK-IN-PROGRESS. DO NOT USE.
#
####################################################################################################

from pathlib import Path
import os.path
from os import path
import sys
from datetime import datetime
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

regex_year = "^[12][0-9]{3}$"
regex_month = "^(0?[1-9]|1[012])$"
regex_time = "([01]\d|2[0-3])[0-5][0-9]"

do {
	user_input_year = Read-Host -Prompt "Enter the year you'd like to create junk events for"
	if (user_input_year -notmatch regex_year) {
		Write-Host "Please enter a valid year between 1000 to 2999" -ForegroundColor Red
	}
} until (user_input_year -match regex_year)

do {
	user_input_month = Read-Host -Prompt "Enter the month you'd like to create junk events for"
	if (user_input_month -notmatch regex_month) {
		Write-Host "Please enter a valid month between 1 to 12" -ForegroundColor Red
	}
} until (user_input_month -match regex_month)

do {
	do {
		user_input_begin_time = Read-Host -Prompt "Enter your start time in 24-hour format without colons (ex: 0830)"
		if (user_input_begin_time -notmatch regex_time) {
			Write-Host "Please enter a valid 24-hour time without colons" -ForegroundColor Red
		}
	} until (user_input_begin_time -match regex_time)

	do {
		user_input_end_time = Read-Host -Prompt "Enter your end time in 24-hour format without colons (ex: 1700)"
		if (user_input_end_time -notmatch regex_time) {
			Write-Host "Please enter a valid 24-hour time without colons" -ForegroundColor Red
		}
	} until (user_input_end_time -match regex_time)

	if (user_input_begin_time -gt user_input_end_time) {
		Write-Host "Start time is later than end time. Please try again" -ForegroundColor Red
	}
} until (user_input_begin_time -lt user_input_end_time)

$DayBeginHour = "user_input_begin_time".toString().Substring(0,2)
$DayBeginMinute = "user_input_begin_time".toString().Substring(2,2)
$DayEndHour = "user_input_end_time".toString().Substring(0,2)
$DayEndMinute = "user_input_end_time".toString().Substring(2,2)

$DaysInMonth = [datetime]::DaysInMonth(user_input_year,user_input_month)

calendar_template_begin = """BEGIN:VCALENDAR
PRODID:-//ZYLAI//iCal Fake Events Generator//EN
VERSION:2.0
METHOD:PUBLISH"""

echo calendar_template_begin >> file_location

for ($Day = 1; $Day -le $DaysInMonth; $Day++) {
	$Date = Get-Date -Year user_input_year -Month user_input_month -Day $Day

	if ($Date.DayOfWeek -eq "Saturday" -Or $Date.DayOfWeek -eq "Sunday") {
		continue
	}

	$DayBegin = Get-Date -Year user_input_year -Month user_input_month -Day $Day -Hour $DayBeginHour -Minute $DayBeginMinute
	$DayEnd = Get-Date -Year user_input_year -Month user_input_month -Day $Day -Hour $DayEndHour -Minute $DayEndMinute

	$EventEnd = $DayBegin

	while ($EventEnd -lt $DayEnd) {
		$BreakLength = New-TimeSpan -Minutes random.choice(break_length_options)
		$EventEnd = $EventEnd + $BreakLength
		$EventBegin = $EventEnd
		$EventLength = New-TimeSpan -Minutes random.choice(event_length_options)
		$EventEnd = $EventBegin + $EventLength

		event_template = """BEGIN:VEVENT
CLASS:PRIVATE
DESCRIPTION:\n
DTSTAMP:$((Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssZ"))
DTSTART:$($EventBegin.ToUniversalTime().ToString("yyyyMMddTHHmm00Z"))
DTEND:$($EventEnd.ToUniversalTime().ToString("yyyyMMddTHHmm00Z"))
PRIORITY:9
SEQUENCE:0
TRANSP:OPAQUE
UID:str(uuid.uuid4())
END:VEVENT"""

		echo event_template >> file_location
	}
}

calendar_template_end = "END:VCALENDAR"

echo calendar_template_end >> file_location

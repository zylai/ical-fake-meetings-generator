# iCal Fake Meetings Generator

Tired of getting pulled into pointless meetings at work? This tool generates realistic-looking fake meetings/events that you can import into your Outlook/Apple/Google calendar to give the impression of how busy you are and prevent people from booking your calendar.

### Now available in Python and PowerShell!

![outlook](https://user-images.githubusercontent.com/40312846/210455165-70c004da-a926-4aa5-9c10-1769dac9724c.png)

## Features
- Fake events generated look just like a normal busy schedule
    - Events are of various lengths and sometimes overlap
- Takes into account your normal start- and end- times
    - Events are sometime scheduled before your normal start time and after your normal end time
- Generates events one month at a time
- Events are marked as busy, private, and show no reminders (so you don't get those pesky reminder pop-ups)
- Weekends are automatically skipped (however, holidays are not taken into account)

The `.ics` file this tool produces adheres to iCalendar specifications, and have been tested on Microsoft Outlook and Apple Calendar, but should work with any calendar that accepts ICS import.

## Instructions

1. Execute the script
    - For Windows users without administrator privileges on their machines, copy and paste the `.ps1` code into PowerShell ISE and execute
    - PowerShell is available for macOS users via Homebrew if you don't have or want to use Python

2. You'll be prompted to enter the year and month you'd like to generate fake events for, as well as your the times you usually start and end your work day. The times must be entered in 24-hour format without colons (for example: 0730, 1700).

```
$ pwsh iCal_Fake_Events_Generator.ps1 
Enter the year you'd like to create junk events for: 2022
Enter the month you'd like to create junk events for: 11
Enter your start time in 24-hour format without colons (ex: 0830): 0800
Enter your end time in 24-hour format without colons (ex: 1700): 1700
iCalendar file generated successfully and has been saved to: /path/to/file
```

3. A file named `calendar.ics` will be created on your desktop (PowerShell version) or home directory (Python version). Preview this file and make sure it is to your liking. If not, simply delete the file and run the script again.

4. Import the `calendar.ics` file to your calendar.

## User-Definable Options

The first three lines of this script can be modified. 

`$FileLocation` specifies the path and name of the output iCal file.

`$BreakLengthOptions` controls the time between events in minutes. Negative values are possible and are used to create events that begin before your normal start time and overlapping events. If you like your breaks to be either 0 or 30 minutes with a 33/67 chance, enter `0,30,30`. This also means that the first meeting/event of your day will either be at your start time (33% chance) or 30 minutes in (67% chance).

`$EventLengthOptions` controls how long meetings are in minutes. Only positive values are possible here. To create events that are 30, 60, or 120 minutes long with a 40/40/20 chance, enter `30,30,60,60,120`.

## To-Do

Update PowerShell version so the UTC conversion is only performed once right after receiving user input and outside the while loop

## Disclaimer

Use this tool responsibly. Don't sue me if you get fired from your job for using this.

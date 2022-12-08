# iCal Fake Meetings Generator

Tired of getting pulled into pointless meetings at work? This tool generates realistic-looking fake meetings/events that you can import into your Outlook/Apple/Google calendar to give the impression of how busy you are and prevent people from booking your calendar.

### Python version coming soon!

## Features
- Fake events generated look just like a normal busy schedule
    - Events are of various lengths and sometimes overlap
- Takes into account your normal start- and end- times
    - Events are sometime scheduled before your normal start time and after your normal end time
    - This is done to simulate realism
- Generates events one month at a time
- Events are marked as busy, private, and show no reminders
- Weekends are automatically skipped (however, holidays are not considered)

The `.ics` file this tool produces adheres to the iCalendar specifications, and have been tested on Microsoft Outlook and Apple Calendar, but should work with any calendar that accept `.ics` import.

## Instructions

1. Execute the script
    - Windows: import the code into PowerShell ISE
    - macOS: [install PowerShell](https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-macos) (available via Homebrew), then execute `pwsh /path/to/file.ps1`

2. You'll be prompted to enter the year and month you'd like to generate fake events for, as well as your the times you usually start and end your work day. The times must be entered in 24-hour format without colons (for example: 0730, 1700).

```
$ pwsh iCal_Fake_Events_Generator.ps1 
Enter the year you'd like to create junk events for: 2022
Enter the month you'd like to create junk events for: 11
Enter your start time in 24-hour format without colons (ex: 0830): 0800
Enter your end time in 24-hour format without colons (ex: 1700): 1700
```

3. A file named `calendar.ics` will be created on your desktop. Preview this file and make sure it is to your liking. If not, simply delete the file and run the script again.

4. Import the `calendar.ics` file to your calendar.

## Disclaimer

Use this tool responsibly. Don't sue me if you get fired from your job for using this.

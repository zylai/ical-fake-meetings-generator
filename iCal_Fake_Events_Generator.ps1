##### User-definable options, start editing here #####

$FileLocation = "$([Environment]::GetFolderPath("Desktop"))\calendar.ics"
$BreakLengthOptions = -90,-60,-30,0,0,0,15,15,15,30,30,60,90
$EventLengthOptions = 15,15,30,30,30,30,30,45,45,60,60,60,60,60,60,60,60,90,90,90,120,120,120,240

##### Start of script, stop editing here #####

$CalendarTemplateBegin=@"
BEGIN:VCALENDAR
PRODID:-//ZYLAI//iCal Fake Events Generator//EN
VERSION:2.0
METHOD:PUBLISH
"@

if (Test-Path -Path $FileLocation -PathType Leaf) {
    Write-Host "An existing iCalendar file is already at: $FileLocation" -ForegroundColor Red
    Write-Host "Delete this file to generate another one. Aborting..." -ForegroundColor Red
    exit 1
}

echo $CalendarTemplateBegin >> $FileLocation

$Msg_Year = "Enter the year you'd like to create junk events for"
$Msg_Month = "Enter the month you'd like to create junk events for"
$Msg_BeginTime = "Enter your start time in 24-hour format without colons (ex: 0830)"
$Msg_EndTime = "Enter your end time in 24-hour format without colons (ex: 1700)"

$RegEx_Year = "^[12][0-9]{3}$"
$RegEx_Month = "^(0?[1-9]|1[012])$"
$RegEx_Time = "([01]\d|2[0-3])[0-5][0-9]"

do {
    $UserInput_Year = Read-Host -Prompt $Msg_Year
    if ($UserInput_Year -notmatch $RegEx_Year) {
        Write-Host "Please enter a valid year between 1000 to 2999" -ForegroundColor Red
    }
} until ($UserInput_Year -match $RegEx_Year)

do {
    $UserInput_Month = Read-Host -Prompt $Msg_Month
    if ($UserInput_Month -notmatch $RegEx_Month) {
        Write-Host "Please enter a valid month between 1 to 12" -ForegroundColor Red
    }
} until ($UserInput_Month -match $RegEx_Month)

do {
    do {
        $UserInput_BeginTime = Read-Host -Prompt $Msg_BeginTime
        if ($UserInput_BeginTime -notmatch $RegEx_Time) {
            Write-Host "Please enter a valid 24-hour time without colons" -ForegroundColor Red
        }
    } until ($UserInput_BeginTime -match $RegEx_Time)

    do {
        $UserInput_EndTime = Read-Host -Prompt $Msg_EndTime
        if ($UserInput_EndTime -notmatch $RegEx_Time) {
            Write-Host "Please enter a valid 24-hour time without colons" -ForegroundColor Red
        }
    } until ($UserInput_EndTime -match $RegEx_Time)

    if ($UserInput_BeginTime -gt $UserInput_EndTime) {
        Write-Host "Start time is later than end time. Please try again" -ForegroundColor Red
    }
} until ($UserInput_BeginTime -lt $UserInput_EndTime)

$DayBeginHour = "$UserInput_BeginTime".toString().Substring(0,2)
$DayBeginMinute = "$UserInput_BeginTime".toString().Substring(2,2)
$DayEndHour = "$UserInput_EndTime".toString().Substring(0,2)
$DayEndMinute = "$UserInput_EndTime".toString().Substring(2,2)

$DaysInMonth = [datetime]::DaysInMonth($UserInput_Year,$UserInput_Month)

for ($Day = 1; $Day -le $DaysInMonth; $Day++) {
    $Date = Get-Date -Year $UserInput_Year -Month $UserInput_Month -Day $Day

    if ($Date.DayOfWeek -eq "Saturday" -Or $Date.DayOfWeek -eq "Sunday") {
        continue
    }

    $DayBegin = Get-Date -Year $UserInput_Year -Month $UserInput_Month -Day $Day -Hour $DayBeginHour -Minute $DayBeginMinute
    $DayEnd = Get-Date -Year $UserInput_Year -Month $UserInput_Month -Day $Day -Hour $DayEndHour -Minute $DayEndMinute

    $EventEnd = $DayBegin

    while ($EventEnd -lt $DayEnd) {
        $BreakLength = New-TimeSpan -Minutes $($BreakLengthOptions | Get-Random)
        $EventEnd = $EventEnd + $BreakLength
        $EventBegin = $EventEnd
        $EventLength = New-TimeSpan -Minutes $($EventLengthOptions | Get-Random)
        $EventEnd = $EventBegin + $EventLength

        $EventTemplate=@"
BEGIN:VEVENT
CLASS:PRIVATE
DESCRIPTION:\n
DTSTAMP:$((Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssZ"))
DTSTART:$($EventBegin.ToUniversalTime().ToString("yyyyMMddTHHmm00Z"))
DTEND:$($EventEnd.ToUniversalTime().ToString("yyyyMMddTHHmm00Z"))
PRIORITY:9
SEQUENCE:0
TRANSP:OPAQUE
UID:$(New-Guid)
END:VEVENT
"@

        echo $EventTemplate >> $FileLocation
    }
}

$CalendarTemplateEnd=@"
END:VCALENDAR
"@

echo $CalendarTemplateEnd >> $FileLocation

Write-Host "iCalendar file generated successfully and has been saved to: $FileLocation" -ForegroundColor Green

exit 0

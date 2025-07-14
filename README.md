# Alarm Clock ⏰

A Python-based Alarm Clock with a CLI version and a GUI built using **Tkinter**.

## Features
- Set multiple alarms with custom labels.
- Repeat alarms daily.
- Snooze alarms.
- Visual real-time clock.
- Plays an alarm sound (`alarm.wav`).

## How to Run
1. Ensure Python is installed on your system.
2. Install required libraries:
3. Run the script:



## Packaging to Executable
You can convert the program to an `.exe` using **PyInstaller**:
pip install pyinstaller
pyinstaller --onefile --noconsole --add-data "alarm.wav;." alarmclock.py
The `.exe` will appear inside the `dist/` folder.


## License
This project is open-source and free to use.

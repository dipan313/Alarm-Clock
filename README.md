# Alarm Clock ⏰

A Python-based Alarm Clock with a CLI version and a GUI built using **Tkinter**.


## 🚀 Features

- ⏰ **Set Multiple Alarms:** Add multiple alarms with custom labels for easy identification.
- 🔁 **Repeat Daily:** Option to repeat alarms every day automatically.
- 🕑 **Snooze Functionality:** Snooze an alarm for 1 minute with a single click.
- 🔕 **Dismiss Alarm:** Instantly stop the ringing alarm.
- 📜 **View & Delete Alarms:** See a list of all set alarms and delete any alarm as needed.
- 🎵 **Custom Alarm Sound:** Alarms ring with a built-in sound (`alarm.wav`).
- 🖥️ **Real-Time Clock:** Displays the current time in HH:MM:SS format.
- 📝 **Labels for Alarms:** Attach custom text labels to each alarm.
- 🖥️ **Graphical User Interface (GUI):** Built with **Tkinter** for an intuitive and user-friendly interface.
- ⚙️ **Command Line Interface (CLI) Version Included:** A CLI version of the alarm clock is included in the same code (commented section) for terminal/console users.


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

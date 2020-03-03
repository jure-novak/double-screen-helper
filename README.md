# Introduction

Double Screen Helper helps musicians display music sheet and lyrics of a music piece on two separate screens.

# Usage

All pairs of music sheet and lyrics have to be in two separate files. Files have to have the same name, except for the string denoting the type of file, i.e.:
- ```Bach minuet lyrics 123.rtf```,
- ```Bach minuet sheet 123.pdf```,

where **the last part of filename** is unique identifying number.

If Anaconda Python distribution is installed, app can be started by double clicking on ```RUN.bat```. If not, just run ```main.py```.

App monitors keyboard for number input. Keyboard input is reset every 2 seconds!
Current numbers are displayed in Command Prompt title.
When enter is pressed, music sheet and lyrics files are opened each on its own monitor.

Press Esc key to close the app.

# Details and requirements
App was developed using [Anaconda](https://www.anaconda.com/distribution/) Python distribution. 

Additionally, these packages have to be installed:
- pynput
- pygetwindow

Windows are moved to selected screens using [Multi Monitor Tool](http://www.nirsoft.net/utils/multi_monitor_tool.html
).
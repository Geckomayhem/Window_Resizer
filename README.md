# Application Window Resizer
A small open-source Windows utility for resizing application windows to common streaming/video resolutions.

Useful for content creators who need to resize games, tools or applications to different resolutions without manually dragging window borders.

## Features
- Resize any open application window by title
- Exact match or partial title matching
- Quick preset buttons
- Dark mode interface
- No installer required
- No telemetry
- No internet access
- No ads
- Open source

## How to run from source
Install Python, then run:
~~~
pip install pygetwindow
python Window_Resizer.py
~~~

## Create the executable yourself
Ensure you run this in the same folder as the Python file:
~~~
pip install pyinstaller pygetwindow
pyinstaller --onefile --windowed --name "Application Window Resizer" Window_Resizer.py
~~~

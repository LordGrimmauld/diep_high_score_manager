# diep_high_score_manager
This is a simple Project to manage game high scores (e.g. diep.io)

Dependencies:
This project is based on Python37. It may or may not run with other Versions of Python.
This project uses the additional Python libraries PIL (pillow) and keyboard.
For the Score recognition, Tesseract-OCR is used. 

Install/dependencies:
Windows is probably required.
the script has to be placed in a directory with a subdirectory called "highscores".
An install of Tesseract-OCR with its dependencies as to be installed in a sub-directory from the scripts directory called "Tesseract-OCR".
Python37 has to be installed.
To install the libraries, open a commandline in the folder of your Python installation and run "python -m pip install pillow, keyboard".

Execution:
To run, simply open the script with the pythonw binary in your Python directory.
The hotkey is "p"

Notes:
In Linux and Mac, the program might work. BUT: You will have to change the command of the OCR, you might have to change the backslashes to normal slashes, and you might require higher privileges then the normal user for running the Python keyboard library.

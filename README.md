# RyanairBot

This bot is written in Python using Selenium webdriver. It crawls through Ryanair website and collects flights' prices for the period specified by user. 

## Requirements
Python version: Python 3.9.12
Dependencies: see requirements.txt file

Firstly, you should create virtual environment and install all required dependencies with commands

*python -m venv /path/to/new/virtual/environment* (venv is the name of the environment)

*./path/to/new/virtual/environment/bin/activate* (activate the environment)

*pip install -r requirements.txt*

## Use Case
When your environment is prepared to run the program type command

*python ./main.py*

Now, you should see the GUI where you can specify flight parameters and your browser (Chrome or Mozilla).
After clicking the conforming button, you'll see the browser window where you can observe the bot in action.
When bot's work is done, a notification is displayed to the user with the lowest price flight. All prices for the given period can be looked up in the report generated under directory */search-reports*.

<img src="https://github.com/Magenta24/RyanairBot/blob/main/screenshots/ryanairBot-GUI.PNG" width="500">
<img src="https://github.com/Magenta24/RyanairBot/blob/main/screenshots/ryanair-bot-report-file.PNG" width="500">
<img src="https://github.com/Magenta24/RyanairBot/blob/main/screenshots/ryanair-bit-console.PNG" width="500">

## Caveats
- The bot was tested on Windows system only
- The path to the Chrome and Mozila drivers need to be specified in Window.py in __init__ function
- In Window.py __init__ uncomment below line to run the bot without opening browser's window 

  *options.add_argument('headless')*
  

# SabermetricsFinalProject
#### Walker Schmidt and Ryan Whitmer
Website to calculate leverage efficiency stat

## How to run
First make sure you can run django with python3 from your machine.
Once the dependecies are installed for django and python3, place pybaseball in /final/home and reinstall it.

Now, to run the server, run the command
~~~~
python3 manage.py runserver
~~~~
from the final/ directory.

## Where to look
Django creates what seems like a mess of files.
For quick reference, look at final/home/templates/index.html for the layout of the html file.
final/stat_calculator is where all of the code will go for calculating the stats.
final/home/views.py is what actaully completes the html and displays what we want.

## Current State
The current state of the project is the minimal amount to be calculating and displaying our new stat. In a rough format, data is collected from statcast and multiple values are used to calculate the new leverage efficiency stat. Short-circuits do not quite work yet, meaning that each page loaded has to pull a full statcast csv from disk. Future plans are to incorporate something like a picture, clean the data, and short-circuit so that the large csv file loading can be bypassed.

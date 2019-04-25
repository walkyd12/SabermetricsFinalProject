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

## Where to go
If you can't figure out Django right away, just focus on getting the stats together. The output format should be a dictionary of player names and their calculated stats. This can be easily implemented and displayed in this website.


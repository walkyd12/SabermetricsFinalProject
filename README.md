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
For quick reference, look at final/home/templates/index.html for the layout of the html file.  
final/stat_calculator is where all of the code will go for calculating the stats.  
final/home/views.py is what actaully completes the html and displays what we want. This is where stat_calculator functions are used.

## Project Overview
The statistic we plan to calculate is a leverage efficiency stat. To calculate this stat we will be using the sum of a player’s situational plays by looking at possible change in win probability compared to conversion on those changes. We will use the actual change in win probability for each play and divide it by the possible change in win probability for that play. This will provide a conversion percentage for win probability, which intends to show how often a player can convert on “clutch” plays given the opportunity. This stat is similar to leverage, win expectancy, and win probability added (wpa). The goal of this statistic is to judge how “clutch” a player is which is a big topic and goal in current baseball analysis. This statistic aims to analyze situations a step beyond the way that leverage looks at situations. Leverage is a pure statistical analysis of how the average team does, given a very particular state of the game. With our leverage efficiency stat, we take into account leverage’s pure statistical analysis of average teams, as well as looking at how often a player may be in high leverage situations and how much of the play they were able to leverage to help their team. An example situation is a high leverage situation, down two, and a player gets one run. This does not fully utilize the leverage of the play, so the player can not be awarded full “use” of the leverage. Therefore, we will look at a system where the calculation takes into account how much of this leverage is “used”. We will also compare this to the total possible leverage as to account for the amount of opportunity a player is given, because some players are seldom in high leverage situations, but we do not believe this means they are less “clutch”.  
There are a lot of situations when knowing how clutch a player is would help  the team enormously. With any sport, but especially baseball since it has such a long season, there are instances that matter far more than others. Being down 2 in a game in the beginning portion of the season holds a lot less importance then being down 2 in the wild card game, where a loss will end your season. When you are in a high importance situation like a late-season game that will get you in or out of the playoffs, or a game 7 in a playoff series, you want your best batter to be batting. It is common knowledge in all sports that the players with the best season statistics aren’t always playing their best in the playoffs. One step further, your best guy might not be able to handle the pressure of high leverage situations in general even if they are usually great. Clayton Kershaw has been one of the best pitchers of the decade but he famously cannot win important playoff games. That’s more colloquial knowledge then concrete in stats but the notion still remains across the sports world. This means that in your higher pressure games you would want to look at the clutch stat to move your lineup around, and move your guys that perform under pressure higher up on the list of batters so they have more at bats and therefore are more likely to be on deck in a clutch situation.  
You also might move your best pitcher back in the rotation, or keep one of your statistically best relievers out, if they have shown they can’t play in the highest leverage situations since these games are way more important to win. Scouts could use this stat too. If you are a playoff likely team and your team is solid but full of guys that don’t do well in important situations a scout would greatly value a guy that can do well in clutch situations. If you don’t have a single pitcher that can handle clutch games then a scout would really make sure they pick up one or two guys that can be subbed in during those games.


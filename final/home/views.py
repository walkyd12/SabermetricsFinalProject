from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.template import Context, Template
import pandas as pd
from pybaseball.lahman import *
from stat_calculator import *
import os

# Renders nav bar on side of page for all pages
# Passed html template with no nav links
# Utilizes get_teams from /FinalProject/final/home/stat_calculator.py
def insert_nav(html):
	sideNavDiv = '<div class="sidenav">'
	
	insertIndex = html.find(sideNavDiv)
	insertIndex = insertIndex + len(sideNavDiv)
	
	start = html[:insertIndex]
	end = html[(insertIndex):len(html)]

	links = '<a href="/home/">Home</a>'

	teamList = get_teams()
	for t in teamList:
		teamID = t
		teamName = teamList[t]
		links = links + '<a href="javascript:goto_team_page(\'' + teamID + '\')">' + teamName + '</a>'

	full = start + links + end

	return full

# Function for the home page request
# Use this page to display any basic info about this project
def index(request):
	tagContents = "CSCI 4831 Sabermetrics Final Project"
	statDesc = 'The stat we calculated is the leverage efficiency stat. This stat aims to better tune the leverage stat and give all players an equal chance at being a "clutch" player.'
	about = "The statistic we plan to calculate is a leverage efficiency stat. To calculate this stat we will be using the sum of a player’s situational plays by looking at possible change in win probability compared to conversion on those changes. We will use the actual change in win probability for each play and divide it by the possible change in win probability for that play. This will provide a conversion percentage for win probability, which intends to show how often a player can convert on “clutch” plays given the opportunity. This stat is similar to leverage, win expectancy, and win probability added (wpa). The goal of this statistic is to judge how “clutch” a player is which is a big topic and goal in current baseball analysis. This statistic aims to analyze situations a step beyond the way that leverage looks at situations. Leverage is a pure statistical analysis of how the average team does, given a very particular state of the game. With our leverage efficiency stat, we take into account leverage’s pure statistical analysis of average teams, as well as looking at how often a player may be in high leverage situations and how much of the play they were able to leverage to help their team. An example situation is a high leverage situation, down two, and a player gets one run. This does not fully utilize the leverage of the play, so the player can not be awarded full “use” of the leverage. Therefore, we will look at a system where the calculation takes into account how much of this leverage is “used”. We will also compare this to the total possible leverage as to account for the amount of opportunity a player is given, because some players are seldom in high leverage situations, but we do not believe this means they are less “clutch”. There are a lot of situations when knowing how clutch a player is would help  the team enormously. With any sport, but especially baseball since it has such a long season, there are instances that matter far more than others. Being down 2 in a game in the beginning portion of the season holds a lot less importance then being down 2 in the wild card game, where a loss will end your season. When you are in a high importance situation like a late-season game that will get you in or out of the playoffs, or a game 7 in a playoff series, you want your best batter to be batting. It is common knowledge in all sports that the players with the best season statistics aren’t always playing their best in the playoffs. One step further, your best guy might not be able to handle the pressure of high leverage situations in general even if they are usually great. Clayton Kershaw has been one of the best pitchers of the decade but he famously cannot win important playoff games. That’s more colloquial knowledge then concrete in stats but the notion still remains across the sports world. This means that in your higher pressure games you would want to look at the clutch stat to move your lineup around, and move your guys that perform under pressure higher up on the list of batters so they have more at bats and therefore are more likely to be on deck in a clutch situation. You also might move your best pitcher back in the rotation, or keep one of your statistically best relievers out, if they have shown they can’t play in the highest leverage situations since these games are way more important to win. Scouts could use this stat too. If you are a playoff likely team and your team is solid but full of guys that don’t do well in important situations a scout would greatly value a guy that can do well in clutch situations. If you don’t have a single pitcher that can handle clutch games then a scout would really make sure they pick up one or two guys that can be subbed in during those games."
	rendered = render_to_string('index.html', { 'HEADER_CONTENT': 'Home', 'TAG_CONTENT': tagContents, 'page_list':{'Walker Schmidt and Ryan Whitmer':'','Our Calculated Stat':statDesc, 'About the Project':about} })
	
	return HttpResponse(insert_nav(rendered))

###############################################################################
# The bulk of the project will happen here
###############################################################################
# This is the view for any of the MLB teams we will look at.
# This file is just for loading the template, but this is
# ultimately where the data will have to be formatted for display.
# A function should be created in /FinalProject/final/home/stat_calculator.py
# for processing data and return it in a nicely formatted way so that it can
# easily be displayed.
#
# Example format:
# +-----------------------------------+
# | player_name | our_calculated_stat |
# +-----------------------------------+
#
# Look in /FinalProject/final/home/stat_calculator.py for calculate_leverage_eff_stat(teamID)

def team(request, teamID):
	get_leverage_index("Top 7", "2", "123", "-4")
	lev = calculate_leverage_eff_stat(teamID)
	player_list = []
	list_list = []
	cwd = os.getcwd()
	for p in lev:
		list_list.append(lev[p])
		player_list.append(p)
		lev[p][2] = str((float(lev[p][3]) - (float(lev[p][1]) - float(lev[p][0]))) / float(lev[p][1]))
	print(lev.values())
	rendered = render_to_string('index.html', { 'HEADER_CONTENT': team_name_lookup(teamID), 'TAG_CONTENT': '', 'player_list':lev, 'list_list':lev  })
	return HttpResponse(insert_nav(rendered))


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
	rendered = render_to_string('index.html', { 'HEADER_CONTENT': 'Home', 'TAG_CONTENT': tagContents, 'page_list':{'Walker Schmidt and Ryan Whitmer':'','Our Calculated Stat':statDesc} })
	
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
	rendered = render_to_string('index.html', { 'HEADER_CONTENT': team_name_lookup(teamID), 'TAG_CONTENT': 'team desc', 'player_list':['hi','hello']  })

	return HttpResponse(insert_nav(rendered))


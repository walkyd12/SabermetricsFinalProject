from pybaseball.lahman import *
import pandas as pd

##################################################################
# get_teams()
#
# returns: dictionary of {'teamID':'teamName'}
#
# This function either creates a local file with all of the team
# ids and names in a comma delimitted format found in
# FinalProject/final/home/local_data/
# or, if this file has already been built, the function reads
# in the data and return it in the same afformentioned format
##################################################################
def get_teams():
	cwd = os.getcwd()
	teamDict = {}
	if os.path.exists(cwd + "/home/local_data/teamDataLocal.txt"):
		file = open(cwd + '/home/local_data/teamDataLocal.txt', 'r')
		line = file.readline()
		cnt = 1
		while line:
			com = line.find(',')
			end = line.find('\n')
			tID = line[0:com]
			name = line[(com+1):end]
			teamDict[tID] = name
			line = file.readline()
		file.close()
	else:
		file = open(cwd + '/home/local_data/teamDataLocal.txt', 'w+')
		print("Creating local team data file...")
		teamList = teams()
		teamNameList = teamList.loc[(teamList["yearID"]==2016),["name", "teamID"]]
		print(teamNameList.head(1))
		for i in range(0, len(teamNameList)):
			teamID = teamNameList['teamID'].values[i]
			teamName = teamNameList['name'].values[i]
			teamDict[teamID] = teamName;
			line = teamID + "," + teamName + "\n"
			file.write(line)
			print(line)
		file.close()

	return teamDict

def team_name_lookup(teamID):
	teams = get_teams()
	return teams[teamID]

#####################################################################
# calculate_leverage_eff_stat(teamID)
# 
# input: ID of team to calculate stats of players
#
# return: a dictionary of playerNames and the calculated stat
#
# This function is where all of the calculations should take place.
# Should return a nicely formatted dictionary similar to 
# +-----------------------------------+
# | player_name | our_calculated_stat |
# +-----------------------------------+
#####################################################################

def calculate_leverage_eff_stat(teamID):
	levEffDict = {}

	# Do the calculations, store in levEffDict


	# Return the final list
	return levEffDict
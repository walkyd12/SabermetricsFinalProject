from pybaseball.lahman import *
from pybaseball import statcast
import pandas as pd
import numpy as np
import math
import csv

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
	if(teamID in teams):
		return teams[teamID]
	else:
		return 'None'

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
	#print(team_name_lookup(teamID))
	statcastData = create_statcast_CSV('2017')
	statcastData = statcastData.loc[((statcastData['home_team'] == teamID) & (statcastData['inning_topbot'] == 'Bot')) | ((statcastData['away_team'] == teamID) & (statcastData['inning_topbot'] == 'Top')), ["batter", "inning", "on_1b", "on_2b", "on_3b", "bat_score", "fld_score", "outs_when_up", "post_bat_score", "post_fld_score", "des"]]

	for i in range (len(statcastData)):
	
		leverageGained = 0
		leveragePossible = 0

		prePlay = dict()
		postPlay = dict()

		prePlay['inning'] = statcastData.iloc[i]['inning']
		prePlay['1b'] = statcastData.iloc[i]['on_1b']
		prePlay['2b'] = statcastData.iloc[i]['on_2b']
		prePlay['3b'] = statcastData.iloc[i]['on_3b']
		prePlay['outs'] = statcastData.iloc[i]['outs_when_up']
		prePlay['playerScore'] = statcastData.iloc[i]['bat_score']
		prePlay['opposingScore'] = statcastData.iloc[i]['fld_score']
		if(not (i==0)):
			if(not pd.isnull(statcastData.iloc[i]['des'])):
				if((not (statcastData.iloc[i]['inning'] == statcastData.iloc[i-1]['inning'])) & (not (statcastData.iloc[i]['inning'] == 9))):

					postPlay['inning'] = prePlay['inning'] + 1
					postPlay['1b'] = np.nan
					postPlay['2b'] = np.nan
					postPlay['3b'] = np.nan
					postPlay['outs'] = 0
					postPlay['playerScore'] = prePlay['playerScore']
					postPlay['opposingScore'] = prePlay['opposingScore']

				else:

					postPlay['inning'] = prePlay['inning']
					postPlay['1b'] = statcastData.iloc[i-1]['on_1b']
					postPlay['2b'] = statcastData.iloc[i-1]['on_2b']
					postPlay['3b'] = statcastData.iloc[i-1]['on_3b']
					postPlay['outs'] = statcastData.iloc[i-1]['outs_when_up']
					postPlay['playerScore'] = statcastData.iloc[i-1]['bat_score']
					postPlay['opposingScore'] = statcastData.iloc[i-1]['fld_score']

					#prePlay is the state of the game before the at-bat
					#postPlay is the state of the game after
					#This is where we compare the leverage change in game state and update it below

				if(statcastData.iloc[i]['batter'] in levEffDict):
					levEffDict[statcastData.iloc[i]['batter']] = (levEffDict[statcastData.iloc[i]['batter']][0] + leverageGained, levEffDict[statcastData.iloc[i]['batter']][1] + leveragePossible, levEffDict[statcastData.iloc[i]['batter']][2] + 1)
				else:		
					levEffDict[statcastData.iloc[i]['batter']] = (leverageGained, leveragePossible, 1)

			else:
				print(statcastData.iloc[i]['des'])

	#setting up levEffDict to be key = batter (mlb player id)
	#value = (total leverage attempted, total leverage gained, total AB)
	#the total leverage attempted is possible leverage this player could have converted if everything went perfectly
	#total leverage gained is what actually happened
	#total AB is their at bats
	#We can then convert to player first and last names with lahman's, and do whatever averaging we wanna do with the value


	# Return the final list
	return levEffDict


def create_statcast_CSV(yearID):

	cwd = os.getcwd()
	if os.path.exists(cwd + "/home/local_data/statcast" + yearID + '.csv'):
		file = pd.read_csv(cwd + "/home/local_data/statcast" + yearID + '.csv')
	else:
		file = statcast(start_dt=yearID + '-04-01', end_dt=yearID + '-11-01')
		pd.DataFrame.to_csv(file, cwd + "/home/local_data/statcast" + yearID + '.csv', ',')

	return file


print(calculate_leverage_eff_stat('SEA'))



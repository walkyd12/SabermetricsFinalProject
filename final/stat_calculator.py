from pybaseball.lahman import *
from pybaseball import *
import pandas as pd
import numpy as np
import math
import csv
import os

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

def player_name_lookup(playerIDs):
	
	nameDF = pd.read_csv('./home/local_data/master.csv', encoding = "ISO-8859-1")

	playerNames = dict()
	for key, val in playerIDs.items():
		newKey = nameDF.loc[(nameDF['mlb_id'] == key)]['mlb_name'].values[0]
		playerNames[newKey] = val

	return playerNames

def team_name_lookup(teamID):
	teams = get_teams()
	if(teamID in teams):
		return teams[teamID]
	else:
		return 'None'

#####################################################################
# def get_leverage_index(inning, outs, bases, scoreDif)
# 
# input: 
# 	inning: The inning formatted in ["Top "/"Bot "][<inning number>]
#			ex. "Top 7" "Bot 2"
# 	outs: Number of outs
#	bases: Runners on base formatted in a 3 character string
#		   use base number if runner on or '_' if empty
#		   ex. "1_3" "___" "12_" "123"
#	scoreDif: the differnce in score (negative means losing)
#
# return: the specific leverage index for the provided situation
#
# This function takes in a game situation and does a lookup in the
# leverage index csv found in FinalProject/final/home/local_data/
#####################################################################
def get_leverage_index(inning, outs, bases, scoreDif):
	cwd = os.getcwd()
	file = open(cwd + '/home/local_data/LeverageIndexData.csv', 'r')
	cnt = 0
	curInning = ''
	finalDict = {}

	line = file.readline()
	while line:
		end = line.find('\n')
		line = line.replace(' ','')

		firstComma = line.find(',')
		if (line.find(',') > 0) and (line.find(',Outs,') < 0):
			inningBot = line.find('Bottom')
			inningTop = line.find('Top')
			if(inningTop >= 0) or (inningBot >= 0):
				if(inningTop >= 0):
					curInning = "Top "+line[firstComma-1]
				else:
					curInning = "Bot "+line[firstComma-1]
				finalDict[curInning] = {}
			else:
				curComma = firstComma
				commaIndexes = [curComma]
				while(curComma > 0):
					nextComma = line.find(',', curComma+1)
					if(nextComma > 0):
						commaIndexes.append(nextComma)
					curComma = nextComma

				lastCom = 0
				for comInd in commaIndexes:
					if(comInd > 3):
						if(comInd == 5):
							finalDict[curInning][str(line[:5])] = []
							lastCom = 5
						else:
							if (lastCom+1) == comInd:
								finalDict[curInning][str(line[:5])].append(0)
							else:
								finalDict[curInning][str(line[:5])].append((float)(line[lastCom+1:comInd]))
							lastCom = comInd
			cnt = cnt + 1
		line = file.readline()

	if(int(scoreDif) < -4):
		scoreDif = -4
	elif(int(scoreDif) > 4):
		scoreDif = 4

	idex = int(scoreDif)+4
	if(idex > 7):
		idex = 7
	if(idex < 0):
		idex = 0
	file.close()

	return finalDict[inning][bases+","+outs][idex]


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
	cwd = os.getcwd()
	
	if os.path.exists(cwd + '/home/local_data/'+teamID+'DataLocal.txt'):
		oldFile = open(cwd + '/home/local_data/'+teamID+'DataLocal.txt', 'r')
		line = oldFile.readline()
		cnt = 1
		while line:
			name = line[:line.find(',')-1]
			levEffDict[name] = line[line.find(','):].split(',')
			line = oldFile.readline()
		oldFile.close()
		return levEffDict

	# Do the calculations, store in levEffDict
	statcastData = create_statcast_CSV('2017')
	statcastData = statcastData.loc[((statcastData['home_team'] == teamID) & (statcastData['inning_topbot'] == 'Bot')) | ((statcastData['away_team'] == teamID) & (statcastData['inning_topbot'] == 'Top')), ["batter", "inning_topbot", "inning", "on_1b", "on_2b", "on_3b", "bat_score", "fld_score", "outs_when_up", "post_bat_score", "post_fld_score", "des"]]
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
		prePlay['inning_topbot'] = statcastData.iloc[i]['inning_topbot']
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
					postPlay['inning_topbot'] = prePlay['inning_topbot']

				else:

					postPlay['inning'] = prePlay['inning']
					postPlay['1b'] = statcastData.iloc[i-1]['on_1b']
					postPlay['2b'] = statcastData.iloc[i-1]['on_2b']
					postPlay['3b'] = statcastData.iloc[i-1]['on_3b']
					postPlay['outs'] = statcastData.iloc[i-1]['outs_when_up']
					postPlay['playerScore'] = statcastData.iloc[i-1]['bat_score']
					postPlay['opposingScore'] = statcastData.iloc[i-1]['fld_score']
					postPlay['inning_topbot'] = prePlay['inning_topbot']

					#prePlay is the state of the game before the at-bat
					#postPlay is the state of the game after
					#This is where we compare the leverage change in game state and update it below

				preBaseString = ''
				postBaseString = ''
				if(prePlay['1b'] > 0):
					preBaseString = preBaseString + '1'
				else:
					preBaseString = preBaseString + '_'
				if(prePlay['2b'] > 0):
					preBaseString = preBaseString + '2'
				else:
					preBaseString = preBaseString + '_'
				if(prePlay['3b'] > 0):
					preBaseString = preBaseString + '3'
				else:
					preBaseString = preBaseString + '_'

				if(postPlay['1b'] > 0):
					postBaseString = postBaseString + '1'
				else:
					postBaseString = postBaseString + '_'
				if(postPlay['2b'] > 0):
					postBaseString = postBaseString + '2'
				else:
					postBaseString = postBaseString + '_'
				if(postPlay['3b'] > 0):
					postBaseString = postBaseString + '3'
				else:
					postBaseString = postBaseString + '_'

				preLeverage = get_leverage_index((str(prePlay['inning_topbot'])+' '+str(prePlay['inning'])[0]), str(prePlay['outs'])[0], preBaseString, str(int(prePlay['playerScore'])-int(prePlay['opposingScore'])))
				postLeverage = get_leverage_index((str(postPlay['inning_topbot'])+' '+str(postPlay['inning'])[0]), str(postPlay['outs'])[0], postBaseString, str(int(postPlay['playerScore'])-int(postPlay['opposingScore'])))

				leverageGained = preLeverage - postLeverage
				leveragePossible = preLeverage

				if(statcastData.iloc[i]['batter'] in levEffDict):
					levEffDict[statcastData.iloc[i]['batter']] = [levEffDict[statcastData.iloc[i]['batter']][0] + leverageGained, levEffDict[statcastData.iloc[i]['batter']][1] + leveragePossible, 0, levEffDict[statcastData.iloc[i]['batter']][3] + 1]
				else:		
					levEffDict[statcastData.iloc[i]['batter']] = [leverageGained, leveragePossible, 0, 1]

	newFile = open(cwd + '/home/local_data/'+teamID+'DataLocal.txt', 'w+')
	print("Creating new local team data file...")
	for batter in levEffDict:
		newLine = str(batter) + ',' + str(levEffDict[batter][0])+ ',' + str(levEffDict[batter][1]) + ',' + str(levEffDict[batter][2]) + str(levEffDict[batter][3])
		newFile.write(newLine)
	newFile.close()
	# Return the final list
	levEffDict = player_name_lookup(levEffDict)

	return levEffDict

#####################################################################
# create_statcast_CSV(yearID)
# 
# input: year the statcast csv data should be creted for
#
# return: contents of yearID's statcast data
# 
#####################################################################
def create_statcast_CSV(yearID):

	cwd = os.getcwd()
	if os.path.exists(cwd + "/home/local_data/statcast" + yearID + 'p1.csv'):
		print("Found CSV file! Reading part 1...")
		file1 = pd.read_csv(cwd + "/home/local_data/statcast" + yearID + 'p1.csv', low_memory=False)
		print("Found CSV file! Reading part 2...")
		file2 = pd.read_csv(cwd + "/home/local_data/statcast" + yearID + 'p2.csv', low_memory=False)
		print("Found CSV file! Reading part 3...")
		file3 = pd.read_csv(cwd + "/home/local_data/statcast" + yearID + 'p3.csv', low_memory=False)
		print("Joining files...")
		file = pd.concat([file1, file2, file3])
	else:
		print("Statcast: "+yearID+" part 1")
		file1 = statcast(start_dt=yearID + '-04-01', end_dt=yearID + '-6-01')
		pd.DataFrame.to_csv(file1, cwd + "/home/local_data/statcast" + yearID + 'p1.csv', ',')
		print("Statcast: "+yearID+" part 2")
		file2 = statcast(start_dt=yearID + '-06-02', end_dt=yearID + '-9-01')
		pd.DataFrame.to_csv(file2, cwd + "/home/local_data/statcast" + yearID + 'p2.csv', ',')
		print("Statcast: "+yearID+" part 3")
		file3 = statcast(start_dt=yearID + '-09-02', end_dt=yearID + '-11-01')
		pd.DataFrame.to_csv(file3, cwd + "/home/local_data/statcast" + yearID + 'p3.csv', ',')
		print("Joining files...")
		file = pd.concat([file1, file2, file3])

	print("Statcast complete!")
	return file
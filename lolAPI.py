import requests
import time
import os
import datetime
import shutil



class RiotEngine():
	uris = {
	'get_summoner_by_name' : '/lol/summoner/v3/summoners/by-name/',
	'get_mastery_by_summ_id' : '/lol/champion-mastery/v3/champion-masteries/by-summoner/',
	'get_all_champ_data' : '/lol/static-data/v3/champions/',
	'get_matchlist_by_account' : '/lol/match/v3/matchlists/by-account/',
	'get_match_by_match_id' : '/lol/match/v3/matches/'
}
	def __init__(self, api_key, region):
		self.api_key = api_key
		self.base_url = 'https://' + region + '.api.riotgames.com'
		self.champFile = '/Users/adamhalfaker/Documents/LeagueProject/champs.json'


	''' 		Helper Functions 		'''
	def response(self,url):
		r = requests.get(url)
		return r.json()
	def convertTimeStamp(self, timestamp, dateFormat=None):
		if (dateFormat == None):
			dateFormat = "%m/%d/%Y"
		d = datetime.datetime.fromtimestamp(float(timestamp/1000.))
		return d.strftime(dateFormat)
	def getChampionImage(self, fileName):
		imgUrl = 'https://ddragon.leagueoflegends.com/cdn/7.10.1/img/champion/' + fileName
		r = requests.get(imgUrl, stream=True)
		with open('/Users/adamhalfaker/Documents/LeagueProject/champ_icons/' + fileName, 'wb') as out_file:
			shutil.copyfileobj(r.raw, out_file)
		del r


	def getSummonerByName(self, name):
		url = self.base_url + self.uris['get_summoner_by_name'] + name + '?' + self.api_key
		return self.response(url)
	def getMasteryBySummId(self, summId):
		url = self.base_url + self.uris['get_mastery_by_summ_id'] + str(summId)  + '?' + self.api_key
		return self.response(url)
	def getMatchlistByAcct(self, account):
		url = self.base_url + self.uris['get_matchlist_by_account'] + str(account) + '?' +self.api_key
		return self.response(url)
	def getMatchByMatchId(self, match_id):
		url = self.base_url + self.uris['get_match_by_match_id'] + str(match_id) + '?' + self.api_key
		return self.response(url)
	def getMatchesByDate(self, date, account):
		matchlist = self.getMatchlistByAcct(account)
		matches = [0]
		for match in matchlist['matches']:
			date_converted = self.convertTimeStamp(match['timestamp'])
			if(date_converted == date):
				matches[0] += 1
				matches.append(self.getMatchByMatchId(match['gameId']))
		return matches
	def getChampionNameByChampId(self, champId):
		url = self.base_url+self.uris['get_all_champ_data'] + str(champId) + '?tags=image&' + self.api_key
		return self.response(url)
	



		










